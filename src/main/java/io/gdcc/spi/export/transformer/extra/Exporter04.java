package io.gdcc.spi.export.transformer.extra;

import com.google.auto.service.AutoService;
import io.gdcc.spi.export.Exporter;
import io.gdcc.spi.export.transformer.TransformerExporter;

/**
 * Transformer exporter holder class.
 * 
 */
// This annotation makes the Exporter visible to Dataverse. How it works is well
// documented on the Internet.
@AutoService(Exporter.class)
// All Exporter implementations must implement this interface or the XMLExporter
// interface that extends it.
public class Exporter04 extends TransformerExporter {
    /**
     * Default constructor
     */
    public Exporter04() {
        super(4);
    }
}
