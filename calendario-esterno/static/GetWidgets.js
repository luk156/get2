/**
 * Created by matteo on 25/04/14.
 */

moment.lang('it');

$.ajaxSetup({
    crossDomain: true
    //,
    //beforeSend: function(xhr, settings) {
    //    var csrftoken = $.cookie('csrftoken');
    //    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //}
});

// controllo Calendario
var Turno = Backbone.Model.extend({});

var turnoWidget = Backbone.View.extend({
    initialize: function(){
        this.model.bind("reset", this.render, this);
        this.render();
    },
    render: function(){
        var self = this;
        var attr = this.model.attributes;
        var inizio = new moment(attr.inizio).format('H:mm');
        var fine = new moment(attr.fine).format('H:mm');
        this.$el.addClass('turno');
        var ht = [''];
        ht.push('<div class="titolo-turno '+(attr.coperto? 'titolo-turno-err':'titolo-turno-ok')+'"><i class="fa fa-clock-o"></i> '+inizio+'-'+fine);
		if(attr.identificativo!='')
			ht.push('<h6 class="turno-identificativo">'+attr.identificativo+'</h6>');
		ht.push('</div>');
        for (var r in attr.requisiti){
            var req = attr.requisiti[r];
            var icona = "fa-"+req.mansione.icona.split("-")[1];
            //ht.push('<div class="mansione-calendario">');
            //ht.push('<h6>'+req.mansione.nome+'</h6>');
            //ht.push('</div>');
            ht.push('<div class="persone"><ul>');
            for (var p in req.disponibilita){
                var persona = req.disponibilita[p];
                ht.push('<li class="persona-turno"><i class="fa '+icona+'" style="color:'+req.mansione.colore+'"></i> '+persona+'</li>');
            }
            ht.push('</ul></div>');
	    
        }
	if(typeof(req.note) != 'undefined'){
		ht.push('<div class="mansione-calendario"><h6> NOTE </h6></div>');
		ht.push('<div class="turno-note">'+req.note+'</div>');		
	}
        ht.push('<div class="footer-turno">'+attr.tipo+'</div>');
        this.$el.html(ht.join(""));
        return this;
    }
});



var Giorno = Backbone.Collection.extend({
    model: Turno
});


var giornoWidget = Backbone.View.extend({
    initialize: function(){
        this.turni=[];
    },

    render: function() {
        this.destroyViews();
        this.turni = this.collection.map(this.createView, this);
        this.$el.append( _.map(this.turni, this.getDom, this) );
    },

    createView: function (model) {
        return new turnoWidget({ model: model });
    },

    getDom: function (view) {
        return view.render().el;
    },

    destroyViews: function() {
        _.invoke(this.turni, 'destroy');
        this.turni.length = 0;
    }

});

var calendarWidget = Backbone.View.extend({
    events: {
        "click .calendario-pager li":  "move"
    },
    initialize: function(options){
        _.bindAll(this, 'redim');
        var self = this;
        this.options = {};
        this.options.n_giorni = 7;
        this.options.cal_id = 1;
        this.options = _.defaults(options || {}, this.options);
        this.giorni = {};
        this.start = new moment();
        this.load(this.render);
    },
    load:  function(cb){
        $('#loading').show();
        var self=this;
        this.giorni = {};
        this.com('init',{
            start: self.start.format('X'),
            stop: moment(self.start).add('days', this.options.n_giorni-1).format('X'),
            cal_id: this.options.cal_id
        },function(data){
            for (var g in data){
                self.giorni[data[g].data] = new giornoWidget({collection: new Giorno(data[g].turni)});
            }
            cb.apply(self);
            $('#loading').hide();
        });
    },
    move: function(ev){
        var dir = $(ev.currentTarget).attr('dir');
        switch (dir){
            case 'avanti':
                this.start.add('days',this.options.n_giorni);
                break;
            case 'indietro':
                this.start.subtract('days',this.options.n_giorni);
                break;
        }
        this.load(this.render);
    },
    render: function(){
        this.$el.html("");
        var ht_pager = '<div class="calendario-pager"><ul class="pager">' +
            '<li class="previous" dir="indietro"><a href="#"><i class="fa fa-chevron-left"></i>  Indietro</a>' +
            '<li class="next" dir="avanti"><a href="#"><i class="fa fa-chevron-right"></i>  Avanti</a>' +
            '</ul></div>';

        this.$el.append(ht_pager);

        for (var giorno in this.giorni){
            var ht = [];
            ht.push('<div class="giorno" id="'+giorno+'">');
            ht.push('<div class="giorno-titolo"><h4>');
            ht.push(new moment(giorno).format('ddd, D MMM'));
            ht.push('</h4></div>');
            ht.push('<div class="turni-container">');
            ht.push('</div>');
            ht.push('</div>');
            this.$el.append(ht.join(""));
            this.giorni[giorno].setElement( $('#'+giorno+' > .turni-container', this.$el) ).render();
        }

        //this.$el.append(ht_pager);
        this.redim();

    },
    com: function(type,data,success_cb,fail_cb){
        $.ajax({
            type: 'post',
            dataType: 'jsonp',
            url:'http://misecampi.gis3w.it//ajax_request/',
            data :{
                control: 'calendar',
                type: type,
                data: JSON.stringify(data),
                apikey: "abc123456789abc"
            }
        }).done(success_cb).fail(fail_cb);
    },
    redim: function(){
        giorno_w = ($(this.el).width()-6*7)/this.options.n_giorni;
        $('.giorno').width(giorno_w);

    }
});
