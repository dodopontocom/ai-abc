const express = require('express');
const stripe = require('./config'); // Importa a configuração do Stripe
const app = express();
const bodyParser = require('body-parser');
require('dotenv').config();

const path = require('path');

// Middleware para processar dados JSON
app.use(express.json());
app.use(bodyParser.json());

app.post('/create-payment-intent', async (req, res) => {
  const { amount } = req.body;

  try {
      // Cria uma PaymentIntent
      const paymentIntent = await stripe.paymentIntents.create({
          amount: amount,
          currency: 'brl',
          payment_method_types: ['card'],
      });

      // Envia o client_secret para o frontend
      res.send({ clientSecret: paymentIntent.client_secret });
  } catch (error) {
      res.status(500).send({ error: error.message });
  }
});

app.get('/config', (req, res) => {
  res.json({ publicKey: process.env.STRIPE_PUBLIC_KEY });
});

// Serve arquivos estáticos da pasta 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Serve a página de seleção de valor
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'options.html'));
});

app.get('/success', (req, res) => {
  res.sendFile(__dirname + '/success.html'); // Substitua pelo caminho real do seu arquivo HTML
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

