const express = require('express');

const app = express();

const PORT = process.env.PORT || 3000;
const HOST = 'localhost';

server = app.listen(PORT, HOST, () => {
    console.log(`\nServer is running at http://${HOST}:${PORT}.`);
    console.log('Testing for 2 seconds...');
});

setTimeout( function() {
    server.close(() => {
        console.log('Express server is working properly. Closed.');
    });
}, 2000);