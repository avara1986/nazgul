# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import datastore

KIND_DATASTORE = "Nazgul"


def get_client():
    return datastore.Client()


def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity


def list_objects(user=None, filters=[], limit=1):
    ds = get_client()

    query = ds.query(kind=KIND_DATASTORE, order=['-timestamp'])
    query.add_filter('user', '=', user)
    for filter in filters:
        query.add_filter(*filter)
    query_iterator = query.fetch(limit=limit)
    page = next(query_iterator.pages)

    entities = list(map(from_datastore, page))

    return entities


# [START update]
def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key(KIND_DATASTORE, int(id))
    else:
        key = ds.key(KIND_DATASTORE)

    entity = datastore.Entity(
        key=key)

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update


def delete(id):
    ds = get_client()
    key = ds.key(KIND_DATASTORE, int(id))
    ds.delete(key)
