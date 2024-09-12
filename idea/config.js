// config.js
require('dotenv').config(); // Carrega variáveis do .env
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
module.exports = stripe;