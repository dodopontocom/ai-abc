import feedparser
from newspaper import Article
import os
import platform
from datetime import datetime
import re
import random
import requests
from bs4 import BeautifulSoup
import sys
import time

# Listas de descritores e sobrenomes para gerar nomes fictícios
descriptors = [
    "sad", "gorgeous", "mysterious", "brilliant", "enigmatic",
    "clever", "famous", "fabulous", "legendary", "witty"
]
surnames = [
    "einstein", "currier", "smith", "rogers", "jones",
    "doe", "watson", "adams", "brown", "clark"
]

# URLs dos RSS feeds que iremos usar
feeds = {
    'Astronomia': [
        'https://www.nasa.gov/rss/dyn/breaking_news.rss',
        'http://rss.sciam.com/ScientificAmerican-Global',
        'https://www.space.com/feeds/all',
    ],
    'Tecnologia': [
        'https://www.techradar.com/rss',
        'http://feeds.arstechnica.com/arstechnica/index',
    ],
    'Xadrez': [
        'https://www.chessbase.com/portals/4/rss/index.xml',
        'https://www.chess.com/news/rss',
        'https://theweekinchess.com/rss',
    ],
    'Futebol': [
        'https://globoesporte.globo.com/rss',
        'https://www.goal.com/en/feeds/news',
    ],
    'Música': [
        'https://www.rollingstone.com/music/music-news/feed/',
        'https://www.nme.com/feed/',
    ],
    'Brasil_Hoje': [
        'https://g1.globo.com/rss/g1.xml',
        'https://feeds.uol.com.br/feed.xml',
        'https://www.cnnbrasil.com.br/feed/',
        'https://feeds.folha.uol.com.br/folha/ultimas/feed.xml',
    ],
}

def check_environment_variables():
    """Verifica se as variáveis de ambiente necessárias estão definidas."""
    if not all([os.getenv('TELEGRAM_TOKEN'), os.getenv('NOTIFICATION_IDS')]):
        print("Erro: As variáveis de ambiente 'TELEGRAM_TOKEN' e 'NOTIFICATION_IDS' devem estar definidas.")
        sys.exit(1)

def create_directory():
    """Cria uma pasta com a data atual no nome."""
    today = datetime.now().strftime('%Y-%m-%d')
    directory = f"articles_{today}"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    return directory

def is_lpr_installed():
    """Verifica se o comando `lpr` está disponível no sistema."""
    return os.system("command -v lpr > /dev/null 2>&1") == 0

def sanitize_filename(filename):
    """Remove caracteres inválidos para nomes de arquivos."""
    return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

def generate_fancy_name():
    """Gera um nome fictício com um predicativo e sobrenome."""
    descriptor = random.choice(descriptors)
    surname = random.choice(surnames)
    return f"{descriptor}_{surname}"

def send_telegram_message(token, chat_id, message, retries=5, delay=20):
    """Envia uma mensagem para um chat do Telegram usando o bot e retorna o status."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    for attempt in range(retries):
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Mensagem enviada com sucesso: {message[:50]}...")  # Exibe os primeiros 50 caracteres da mensagem
            return response.json()
        else:
            print(f"Tentativa {attempt + 1} falhou. Status code: {response.status_code}")
            time.sleep(delay)  # Aguarda antes de tentar novamente
    print(f"Erro ao enviar mensagem após {retries} tentativas. Status code final: {response.status_code}")
    return response.json()

def scrape_pilar_news():
    """Faz web scraping no site Pilar News e coleta notícias."""
    url = 'https://www.pilarnews.com.br/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        print(soup.prettify())  # Exibir o HTML da página para verificar a estrutura

        for item in soup.find_all('h2', class_='post-title'):  # Ajuste a classe ou o seletor
            a_tag = item.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag['href']
                articles.append((title, link))
        
        if not articles:
            print("Nenhum artigo encontrado no site Pilar News.")
            with open("error_log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - Erro: Nenhum artigo encontrado no site Pilar News.\n")
        
        return articles

    except Exception as e:
        print(f"Erro ao acessar o site Pilar News: {e}")
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Erro ao acessar o site Pilar News: {e}\n")
        return []

def fetch_random_articles():
    """Coleta um artigo aleatório de cada feed e envia para o Telegram."""
    directory = create_directory()
    
    # Variáveis de ambiente para o Telegram
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('NOTIFICATION_IDS')

    all_articles = {}
    all_tags = set()

    for category, urls in feeds.items():
        # Escolher um feed aleatório para cada categoria
        feed_url = random.choice(urls)
        print(f'\n## {category} ## - Feed: {feed_url}\n')
        
        feed = feedparser.parse(feed_url)
        if feed.entries:
            print(f"Total de artigos encontrados no feed {category}: {len(feed.entries)}")
            entry = random.choice(feed.entries)  # Escolhe um artigo aleatório
            print(f"- {entry.title}\n  {entry.link}\n")
            
            try:
                article = Article(entry.link)
                article.download()
                article.parse()

                text = article.text.strip().replace('\n\n', '\n')
                if len(text) < 100:
                    print(f"Artigo muito curto, possivelmente não foi extraído corretamente: {entry.link}")
                    continue
                
                if article.authors:
                    authors = "_".join(article.authors).replace(" ", "_")
                else:
                    authors = generate_fancy_name()

                base_filename = f"{category}_{authors}_{entry.title[:30]}"
                filename = sanitize_filename(base_filename) + ".txt"
                filepath = os.path.join(directory, filename)
                
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(f"Título: {article.title}\n")
                    file.write(f"URL: {entry.link}\n\n")
                    file.write(text)
                
                all_articles[category] = (article.title, entry.link)
                all_tags.add(category)
                
                if platform.system() == "Linux" or platform.system() == "Darwin":
                    if is_lpr_installed():
                        os.system(f"lpr {filepath}")
                    else:
                        print("Erro: o comando 'lpr' não foi encontrado.")
                elif platform.system() == "Windows":
                    os.startfile(filepath, "print")
            
            except Exception as e:
                print(f"Erro ao processar o artigo: {e}")

    # Adicionar artigos do Pilar News
    pilar_articles = scrape_pilar_news()
    if pilar_articles:
        pilar_article = random.choice(pilar_articles)
        pilar_filename = os.path.join(directory, 'pilarnews_hoje.txt')
        with open(pilar_filename, "w", encoding="utf-8") as file:
            file.write(f"Título: {pilar_article[0]}\n")
            file.write(f"URL: {pilar_article[1]}\n")
        all_articles['Pilar News'] = pilar_article
        all_tags.add('Pilar News')
    
    # Criar e enviar mensagens para o Telegram
    if all_articles:
        tags_message = f"Tags: {', '.join(sorted(all_tags))}"
        
        # Enviar mensagem de tags para o Telegram
        if telegram_token and telegram_chat_id:
            send_telegram_message(telegram_token, telegram_chat_id, tags_message)

        # Enviar mensagem de artigos para o Telegram
        articles_message = "\n\n".join([f"*{category}*\n{title}\n{link}" for category, (title, link) in all_articles.items()])
        if telegram_token and telegram_chat_id:
            send_telegram_message(telegram_token, telegram_chat_id, articles_message)

if __name__ == '__main__':
    check_environment_variables()
    fetch_random_articles()
