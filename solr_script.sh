curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"itemid","indexed": true, "multiValued": false, "type": "plongs"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"brand", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"price", "multiValued": false, "type": "pdoubles"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"price_before_discount", "multiValued": false, "type": "pdoubles"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"currency", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"raw_discount", "multiValued": false, "type": "pdoubles"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"item_rating", "multiValued": false, "type": "pdoubles"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"liked_count", "multiValued": false, "type": "plongs"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"name", "multiValued": false, "type": "text_en", "indexed": false}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"name_tokenized", "multiValued": false, "type": "text_en", "indexed": true, "stored": false}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"shopid", "multiValued": false, "type": "plongs"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"options", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"sex", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"categories", "multiValued": true, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"description", "multiValued": false, "type": "text_en", "indexed": false}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"post_url", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"images", "multiValued": true, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"platform", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"shopid", "multiValued": false, "type": "plongs", "indexed": true}}' http://localhost:8983/solr/multimedia_shops/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"name", "multiValued": false, "type": "text_en", "indexed": false}}' http://localhost:8983/solr/multimedia_shops/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"rating_star", "multiValued": false, "type": "pdoubles"}}' http://localhost:8983/solr/multimedia_shops/schema
curl -X POST -H 'Content-type:application/json' --data-binary '{"add-field":{"name":"platform", "multiValued": false, "type": "text_en"}}' http://localhost:8983/solr/multimedia_shops/schema
