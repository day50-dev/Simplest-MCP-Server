This is the version with an LLM. The LLM here is a local, cpu run version of Qwen3 0.6B. This is a rather unambitious LLM and you don't need any graphics hardware, really powerful machine, API key or need to pay any money.

It will however, require about 4GB disk space all in.

Run

```bash
$ python3 llm_server.py
```

in one terminal to start the server up, or just `^Z` it to the background.

Then run 

```bash
$ python3 test_mcp.py
```

As before
