# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nailgun.extensions import BaseExtension
from nailgun.extensions import BaseExtensionPipeline

from bareon_fuel_extension.adapters import BareonAPIAdapter


BAREON_ADAPTER = BareonAPIAdapter()


class BareonExtensionPipeline(BaseExtensionPipeline):

    @classmethod
    def process_provisioning(cls, provisionig_data, **kwargs):
        for node in provisionig_data['nodes']:
            node['ks_meta']['pm_data'].pop('ks_spaces', None)
            node['partitioning'] = BAREON_ADAPTER.disks(node['uid'])


class BareonExtension(BaseExtension):
    name = 'bareon'
    version = '1.0.0'
    provides = (
        'get_node_volumes',
        'get_node_simple_volumes',
    )
    data_pipelines = (BareonExtensionPipeline,)

    @classmethod
    def get_node_volumes(cls, node):
        return BAREON_ADAPTER.disks(node.id)

    @classmethod
    def get_node_simple_volumes(cls, node):
        "Simple means: 'in simple nailgun format for fuel-agent'"
        return BAREON_ADAPTER.partitioning(node.id)

    @classmethod
    def _put_disks(cls, node):
        disks = []
        for disk in map(lambda d: d.render(), node.volume_manager.disks):
            disk['device'] = disk['name']
            disks.append(disk)

        BAREON_ADAPTER.disks(node.id, data=disks)

    @classmethod
    def on_node_update(cls, node):
        if not BAREON_ADAPTER.exists(node.id):
            cls.on_node_create(node)
        else:
            cls._put_disks(node)

    @classmethod
    def on_node_collection_delete(cls, node_ids):
        for node_id in node_ids:
            BAREON_ADAPTER.delete_node(node_id)

    @classmethod
    def on_node_delete(cls, node):
        BAREON_ADAPTER.delete_node(node.id)

    @classmethod
    def on_node_reset(cls, node):
        cls.on_node_delete(node)

    @classmethod
    def on_node_create(cls, node):
        BAREON_ADAPTER.create_node({'id': node.id})
        cls._put_disks(node)
