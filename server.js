const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');

const { background_worker, init, start, stop } = require('./backgroundworker.js');
const { runner } = require('./python_activator.js');

const PORT = process.env.PORT || 3000;
const HOST = 'localhost';

const app = express();

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));

var clients = {};
var hash_len = 10;
var file_lifetime = 90000;
var extension = '.jpeg';
var checking_folder = './public/clients_images/';

app.get('/', (req, res) => {
    res.render('index', { waitingFlag: false }, function (err, html) {
        res.send(html);
    });
});

app.get('/generator', (req, res) => {

    var client_id = make_id(hash_len);
    clients[client_id] = runner(client_id, req.query.category, req.query.desc, req.query.lang);

    stop();
    start(clients, file_lifetime);

    wait_for_image(client_id)
        .then(function () {
            res.render('index', { image_name: (client_id + extension) }, function (err, html) {
                res.send(html);
            });
        })
        .catch(function (err) {
            handleError(err);
        });
});

app.get('*', (req, res) => {
    res.status(404).send('Serwer po ' + (file_lifetime / 1000.0).toString() + ' sekundach (od uzyskania grafiki) usuwa obraz ze swoich zasobów!');
});

app.listen(PORT, HOST, () => {
    console.log(`Server is running at http://${HOST}:${PORT}.`);

    init(clients, file_lifetime);
    background_worker(clients, file_lifetime);
});

function make_id(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) { result += characters.charAt(Math.floor(Math.random() * charactersLength)); }
    return result;
}

async function wait_for_image(img_name, ext=extension) {
    while (true) {
        try { if (fs.existsSync(checking_folder + img_name + ext)) { break; }
        } catch(err) { console.log('Some error occured: there is no image!'); }
    }
}