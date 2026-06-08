const express = require('express');
const whatsappClient = require('../core/whatsapp_client');

const router = express.Router();

router.post('/send', async (req, res) => {
    const { chatId, text } = req.body;
    if (!chatId || !text) {
        return res.status(400).send('Missing chatId or text');
    }

    try {
        await whatsappClient.sendMessage(chatId, text);
        res.status(200).send('Message sent successfully');
    } catch (e) {
        console.error('Failed to send text:', e);
        res.status(500).send('Error sending text');
    }
});

router.post('/send_file', async (req, res) => {
    const { chatId, filePath } = req.body;
    if (!chatId || !filePath) {
        return res.status(400).send('Missing chatId or filePath');
    }

    try {
        await whatsappClient.sendVoiceNote(chatId, filePath);
        res.status(200).send('Voice note sent successfully');
    } catch (e) {
        console.error('Failed to send voice note:', e);
        res.status(500).send('Error sending voice note');
    }
});

module.exports = router;
