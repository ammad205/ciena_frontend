package org.elasticsearch.river.cassandra;

import org.elasticsearch.common.inject.AbstractModule;
import org.elasticsearch.river.River;

/* 
 * CLASS: CassandraRiverModule
 * the main class of the cassandra river 
 * creates a singleton class object
 */
public class CassandraRiverModule extends AbstractModule {

    @Override
    protected void configure() {
        bind(River.class).to(CassandraRiver.class).asEagerSingleton();
    }
}
