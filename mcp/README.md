# Use the Actors from an MCP client

Apify's hosted MCP server can run any Actor by name. Example client config (Cursor and other clients that accept a remote MCP URL with headers):

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=datawharf-tools/sec-edgar-api,datawharf-tools/eu-ted-tenders,datawharf-tools/sam-gov-opportunities,datawharf-tools/research-search",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

Replace `YOUR_APIFY_TOKEN` with your own token. Check Apify's MCP documentation for the current URL parameters and OAuth option: https://docs.apify.com/platform/integrations/mcp
