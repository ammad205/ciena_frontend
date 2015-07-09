package org.elasticsearch.plugin.river.cassandra;

import org.elasticsearch.common.inject.Inject;
import org.elasticsearch.plugins.AbstractPlugin;
import org.elasticsearch.river.RiversModule;
import org.elasticsearch.river.cassandra.CassandraRiverModule;

public class CassandraRiverPlugin extends AbstractPlugin {

    @Inject
    public CassandraRiverPlugin() {
    }

    @Override
    public String name() {
        return "river-cassandra";
    }

    @Override
    public String description() {
        return "River Cassandra plugin";
    }

    /**
     * Registers the {@link CassandraRiverModule}
     * @param module the elasticsearch module used to handle rivers
     */
    public void onModule(RiversModule module) {
        module.registerRiver("cassandra", CassandraRiverModule.class);
    }
}
