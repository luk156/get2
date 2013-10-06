# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mansione'
        db.create_table(u'persone_mansione', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('descrizione', self.gf('django.db.models.fields.TextField')()),
            ('icona', self.gf('django.db.models.fields.TextField')(default='icon-user')),
            ('colore', self.gf('django.db.models.fields.TextField')(default='#aaa')),
            ('padre', self.gf('persone.models.SelfForeignKey')(blank=True, related_name='children', null=True, to=orm['persone.Mansione'])),
        ))
        db.send_create_signal(u'persone', ['Mansione'])

        # Adding model 'Persona'
        db.create_table(u'persone_persona', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='pers_user', unique=True, null=True, to=orm['auth.User'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cognome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('indirizzo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('nascita', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('tel1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tel2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('stato', self.gf('django.db.models.fields.CharField')(default='disponibile', max_length=40)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notificaMail', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('giorniNotificaMail', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2, null=True, blank=True)),
        ))
        db.send_create_signal(u'persone', ['Persona'])

        # Adding M2M table for field competenze on 'Persona'
        m2m_table_name = db.shorten_name(u'persone_persona_competenze')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persona', models.ForeignKey(orm[u'persone.persona'], null=False)),
            ('mansione', models.ForeignKey(orm[u'persone.mansione'], null=False))
        ))
        db.create_unique(m2m_table_name, ['persona_id', 'mansione_id'])

        # Adding model 'Gruppo'
        db.create_table(u'persone_gruppo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'persone', ['Gruppo'])

        # Adding M2M table for field componenti on 'Gruppo'
        m2m_table_name = db.shorten_name(u'persone_gruppo_componenti')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gruppo', models.ForeignKey(orm[u'persone.gruppo'], null=False)),
            ('persona', models.ForeignKey(orm[u'persone.persona'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gruppo_id', 'persona_id'])


    def backwards(self, orm):
        # Deleting model 'Mansione'
        db.delete_table(u'persone_mansione')

        # Deleting model 'Persona'
        db.delete_table(u'persone_persona')

        # Removing M2M table for field competenze on 'Persona'
        db.delete_table(db.shorten_name(u'persone_persona_competenze'))

        # Deleting model 'Gruppo'
        db.delete_table(u'persone_gruppo')

        # Removing M2M table for field componenti on 'Gruppo'
        db.delete_table(db.shorten_name(u'persone_gruppo_componenti'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'persone.gruppo': {
            'Meta': {'object_name': 'Gruppo'},
            'componenti': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'componenti_gruppo'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['persone.Persona']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'persone.mansione': {
            'Meta': {'object_name': 'Mansione'},
            'colore': ('django.db.models.fields.TextField', [], {'default': "'#aaa'"}),
            'descrizione': ('django.db.models.fields.TextField', [], {}),
            'icona': ('django.db.models.fields.TextField', [], {'default': "'icon-user'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'padre': ('persone.models.SelfForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['persone.Mansione']"})
        },
        u'persone.persona': {
            'Meta': {'object_name': 'Persona'},
            'cognome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'competenze': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['persone.Mansione']", 'null': 'True', 'blank': 'True'}),
            'giorniNotificaMail': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indirizzo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nascita': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notificaMail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stato': ('django.db.models.fields.CharField', [], {'default': "'disponibile'", 'max_length': '40'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pers_user'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['persone']