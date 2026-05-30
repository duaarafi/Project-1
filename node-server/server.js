const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Node.js server is running!');
});

app.listen(3000, () => {
    console.log('Node server running on http://localhost:3000');
});