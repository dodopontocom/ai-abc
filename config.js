require('dotenv').config();

module.exports = {
    stripeSecretKey: process.env.STRIPE_SECRET_KEY,
    stripePublicKey: process.env.STRIPE_PUBLIC_KEY,
};