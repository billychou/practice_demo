#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.query import QuerySet
from django.db import router


class BaseManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return BaseQuerySet(self.model)

    def use_master(self):
        """
        返回当前model对应主库的QuerySet
        """
        return self.get_query_set().use_master()


class BaseQuerySet(QuerySet):

    def use_master(self):
        """
        返回当前model对应主库的QuerySet
        """
        write_db = router.db_for_write(self.model)
        return self.using(write_db)


class BaseModel(models.Model):

    objects = BaseManager()

    class Meta:
        abstract = True

    @classmethod
    def reverse_query_by_uid(cls, uid):
        '''通过uid反查当前class对应的queryset，用于替代xxx_set的地方'''
        return cls.objects.filter(user_id=uid)
