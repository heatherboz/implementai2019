const express = require('express');
const bodyParser = require("body-parser");
const app = express();
const server = app.listen(3000);

const MongoClient = require('mongodb').MongoClient;
const url = "mongodb://localhost:27017/";

app.use(express.static(__dirname + '/public'));
app.set('view engine', 'ejs');

app.get('/', function(req, res){
  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db("fall");
    var query = { fallen: true };
    dbo.collection("montreal_falls").find(query).toArray(function(err, result) {
      if (err) throw err;
      res.render('index', { data: result} );
      db.close();
    });
  });
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

