# Multi-stage build for ENCT enchub server
# Stage 1: Builder
FROM golang:1.22-alpine AS builder

RUN apk add --no-cache git ca-certificates

WORKDIR /build

# Copy engine and enchub modules
COPY src/engine/  ./engine/
COPY src/enchub/  ./enchub/

WORKDIR /build/enchub

# Build the enchub binary
RUN go build -o /enchub .

# Stage 2: Runtime
FROM alpine:3.19

RUN apk add --no-cache ca-certificates

# Create non-root user
RUN adduser -D enct

# Copy binary from builder
COPY --from=builder /enchub /usr/local/bin/enchub

# Set environment variables with defaults
ENV PORT=8080
ENV LEDGER_PATH=/data/ledger
ENV BOOTSTRAP_LOGS_PATH=/data/bootstrap-logs

# Create data directories
RUN mkdir -p /data/ledger /data/bootstrap-logs && \
    chown -R enct:enct /data

# Switch to non-root user
USER enct

WORKDIR /data

# Expose the default port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${PORT}/health || exit 1

# Start enchub
ENTRYPOINT ["/usr/local/bin/enchub"]
