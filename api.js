var express = require('express');
var mongojs = require('mongojs')
var app = express();

var db = mongojs('testdb', ['businesscollection'])

app.get('/', function (req, res) {
	res.send({'methods':['/<ZIPCODE>/<PAGE>','/zips']});
});
app.get('/zips', function (req, res) {
	db.businesscollection.distinct('zipcode',{},
		function(err,list){
			res.send(list);
		})
});

app.get('/:zip/:page', function (req, res) {
	db.businesscollection.find({'zipcode':req.params.zip})
	.limit(5)
	.skip(5*(req.params.page-1),function(err,docs){
		res.send(docs);
	})
});

var server = app.listen(3000, function () {
	var host = server.address().address;
	var port = server.address().port;

});