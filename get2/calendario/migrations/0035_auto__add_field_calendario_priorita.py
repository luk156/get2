# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Calendario.priorita'
        db.add_column(u'calendario_calendario', 'priorita',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Calendario.priorita'
        db.delete_column(u'calendario_calendario', 'priorita')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'calendario.calendario': {
            'Meta': {'object_name': 'Calendario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'priorita': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'calendario.disponibilita': {
            'Meta': {'ordering': "['mansione']", 'object_name': 'Disponibilita'},
            'creata_da': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creata_da_disponibilita'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mansione_disponibilita'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['calendario.Mansione']"}),
            'note': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persona_disponibilita'", 'to': u"orm['calendario.Persona']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'turno_disponibilita'", 'to': u"orm['calendario.Turno']"}),
            'ultima_modifica': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'calendario.gruppo': {
            'Meta': {'object_name': 'Gruppo'},
            'componenti': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'componenti_gruppo'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['calendario.Persona']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'calendario.impostazioni_notifica': {
            'Meta': {'object_name': 'Impostazioni_notifica'},
            'giorni': ('get2.calendario.models.MultiSelectField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo_turno': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['calendario.TipoTurno']", 'null': 'True', 'blank': 'True'}),
            'utente': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impostazioni_notifica_utente'", 'to': u"orm['auth.User']"})
        },
        u'calendario.log': {
            'Meta': {'object_name': 'Log'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'calendario.mansione': {
            'Meta': {'object_name': 'Mansione'},
            'colore': ('django.db.models.fields.TextField', [], {'default': "'#aaa'"}),
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'icona': ('django.db.models.fields.TextField', [], {'default': "'icon-user'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'calendario.notifica': {
            'Meta': {'object_name': 'Notifica'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'destinatario': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinatario_user'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'testo': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'calendario.occorrenza': {
            'Meta': {'object_name': 'Occorrenza'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'calendario.persona': {
            'Meta': {'object_name': 'Persona'},
            'cognome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'competenze': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['calendario.Mansione']", 'null': 'True', 'blank': 'True'}),
            'giorniNotificaMail': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nascita': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notificaMail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retraining': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retraining_blsd': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stato': ('django.db.models.fields.CharField', [], {'default': "'disponibile'", 'max_length': '40'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pers_user'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'calendario.requisito': {
            'Meta': {'object_name': 'Requisito'},
            'extra': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mansione': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'req_mansione'", 'to': u"orm['calendario.Mansione']"}),
            'massimo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'minimo': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'necessario': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sufficiente': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tipo_turno': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'req_tipo_turno'", 'to': u"orm['calendario.TipoTurno']"})
        },
        u'calendario.tipoturno': {
            'Meta': {'object_name': 'TipoTurno'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'msg_errore': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'priorita': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'calendario.turno': {
            'Meta': {'object_name': 'Turno'},
            'calendario': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['calendario.Calendario']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'fine': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificativo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'inizio': ('django.db.models.fields.DateTimeField', [], {}),
            'occorrenza': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['calendario.Occorrenza']", 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['calendario.TipoTurno']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'valore': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['calendario']