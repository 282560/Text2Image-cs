const fs = require('fs');

var working = undefined;
var file_lifetime = undefined;

var clients = {};

var sleep_time = 500;
var checking_folder = './public/clients_images/';

function background_worker (users, f_time) {
    clients = users;
    file_lifetime = f_time;

    (async () => {
        while(working) {
            var clientsNumber = Object.keys(clients).length;
            console.log('The number of objects present on the server: ' + clientsNumber);

            if (!working) { break; }

            var now = Date.now();
            for (var key in clients) {
                if (clients.hasOwnProperty(key)) {
                    if ((now - clients[key]) > file_lifetime) {
                        const human_readable_date = new Date(clients[key]).toString().replace(/T/, ' ').replace(/\..+/, '');
                        console.log('Deleting object: ' + key + ', created at: ' + human_readable_date + '.');

                        fs.unlinkSync(checking_folder + key + '.jpeg');

                        delete clients[key];
                    }
                }
            }
            await new Promise(resolve => setTimeout(resolve, sleep_time));
        }
    })();
};


function init(users, f_time) {
    clients = users;
    file_lifetime = f_time;
    working = true;
}

function start(users, f_time) {
    clients = users;
    file_lifetime = f_time;
    working = true;
}

function stop() {
    working = false;
}

module.exports = { background_worker, init, start, stop };