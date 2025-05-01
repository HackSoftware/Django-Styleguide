# Setting up MCP Documentation Server

This guide explains how to set up the MCP documentation server for the Django Styleguide, which allows IDEs like Cursor and Windsurf to access the documentation context.

## Overview

We use [mcpdoc](https://github.com/langchain-ai/mcpdoc) to expose our `llms.txt` documentation index to IDEs. This allows for better context when working with the Django Styleguide.

## Installation

1. First, install mcpdoc:

```bash
pip install mcpdoc
```

2. Configure your IDE to use the MCP server:

### For Cursor

1. Open Cursor settings and navigate to the MCP configuration
2. Create or edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "django-styleguide-docs-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "DjangoStyleguide:https://raw.githubusercontent.com/HackSoftware/Django-Styleguide/master/llms.txt",
        "--transport",
        "stdio"
      ]
    }
  }
}
```


3. Update Cursor Global Rules (Settings/Rules) with:

```
for ANY question about Django Styleguide, use the django-styleguide-docs-mcp server to help answer -- 
+ call list_doc_sources tool to get the available llms.txt file
+ call fetch_docs tool to read it
+ reflect on the urls in llms.txt 
+ reflect on the input question 
+ call fetch_docs on any urls relevant to the question
+ use this to answer the question
```

### For Windsurf

1. Open Cascade with `CMD+L` (on Mac)
2. Click Configure MCP to open `~/.codeium/windsurf/mcp_config.json`
3. Add the same configuration as shown above for Cursor
4. Update Windsurf Rules/Global rules with the same rule pattern shown above

### For Claude Desktop

1. Open Settings/Developer to update `~/Library/Application\ Support/Claude/claude_desktop_config.json`
2. Add the same configuration as shown above
3. Restart Claude Desktop app

Note: Currently, Claude Desktop doesn't support global rules, so you'll need to include the rules in your prompts:

```
<rules>
for ANY question about Django Styleguide, use the django-styleguide-docs-mcp server to help answer -- 
+ call list_doc_sources tool to get the available llms.txt file
+ call fetch_docs tool to read it
+ reflect on the urls in llms.txt 
+ reflect on the input question 
+ call fetch_docs on any urls relevant to the question
</rules>
```

### For Claude Code

In a terminal after installing Claude Code, run:

```bash
claude mcp add-json django-styleguide-docs '{"type":"stdio","command":"uvx" ,"args":["--from", "mcpdoc", "mcpdoc", "--urls", "DjangoStyleguide:https://raw.githubusercontent.com/HackSoftware/Django-Styleguide/master/llms.txt"]}' -s local
```

## Testing the Setup

To test if the setup is working:

1. Open your IDE
2. Ask a question about the Django Styleguide
3. The IDE should use the MCP server to fetch relevant documentation and provide context-aware answers

## Troubleshooting

If you run into issues with Python version incompatibility, you can explicitly specify the filepath to the Python executable in the `uvx` command:

```json
{
  "mcpServers": {
    "django-styleguide-docs-mcp": {
      "command": "uvx",
      "args": [
        "--python",
        "/path/to/python",
        "--from",
        "mcpdoc",
        "mcpdoc",
        "--urls",
        "DjangoStyleguide:https://raw.githubusercontent.com/HackSoftware/Django-Styleguide/master/llms.txt",
        "--transport",
        "stdio",
        "--port",
        "8082",
        "--host",
        "localhost"
      ]
    }
  }
}
```