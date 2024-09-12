const express = require('express');
const router = express.Router();
const stripe = require('./config');

router.post('/pagar', async (req, res) => {
    const { amount, token } = req.body;

    try {
        const charge = await stripe.charges.create({
            amount: amount,
            currency: 'brl',
            source: token,
        });
        res.json({ message: 'Pagamento realizado com sucesso' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Erro ao processar o pagamento' });
    }
});
