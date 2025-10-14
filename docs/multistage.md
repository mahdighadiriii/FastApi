Normal vs Multi-Stage Docker Build

Normal (Single-Stage):
- One image layer.
- Includes build tools in final image.
- Pros: Simple.
- Cons: Large size, slow, insecure (extra packages).

Multi-Stage:
- Separate build and run stages.
- Copy only runtime files.
- Pros: Small, fast, secure.
- Cons: More complex write.

From Docker docs: Use multi for prod to cut size 90%.
Sources: docker.com, medium.com/docker-multi-stage.