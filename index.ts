import express from 'express';
import mysql from 'mysql2/promise';

const app = express();
const port = 3000;

// Configuração da conexão com o banco de dados (substitua pelas suas credenciais)
const pool = mysql.createPool({
  host: 'seu_host',
  user: 'seu_usuario',
  password: 'sua_senha',
  database: 'seu_banco_de_dados'
});

// Rota para criar uma nova mensagem
app.post('/mensagens', async (req, res) => {
  // ... lógica para inserir a mensagem no banco de dados
});

// Rota para gerar um QR code
app.get('/qrcodes/:id', async (req, res) => {
  // ... lógica para gerar o QR code e enviá-lo para o cliente
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
