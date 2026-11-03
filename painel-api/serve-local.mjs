// Servidor local de teste da API (sem Cloudflare): node serve-local.mjs
import http from "node:http";
import worker from "./worker.js";
const store = new Map();
const PAINEL = { async get(k, t) { const v = store.get(k); if (v === undefined) return null; return t === "json" ? JSON.parse(v) : v; }, async put(k, v) { store.set(k, v); }, async delete(k) { store.delete(k); }, async list({ prefix }) { return { keys: [...store.keys()].filter(k => k.startsWith(prefix)).map(name => ({ name })) }; } };
const env = { PAINEL, GITHUB_REPO: "x/y", BRANCH: "main", SITE_ORIGIN: "http://localhost:3500", MAIL_FROM: "a@b", JWT_SECRET: "segredo-local", GITHUB_TOKEN: "t" };
await PAINEL.put("user:nexus", JSON.stringify({ login: "nexus", nome: "Nexus Digital", email: "nexusdigitalgrp@gmail.com", papel: "admin", criado: 0, versao: 1 }));
await PAINEL.put("reset:tok123", JSON.stringify({ login: "nexus", exp: 9999999999 }));
http.createServer(async (req, res) => {
  let body = ""; for await (const c of req) body += c;
  const r = await worker.fetch(new Request("http://127.0.0.1:8787" + req.url, { method: req.method, headers: req.headers, body: ["GET", "HEAD", "OPTIONS"].includes(req.method) ? undefined : body }), env);
  res.writeHead(r.status, Object.fromEntries(r.headers)); res.end(Buffer.from(await r.arrayBuffer()));
}).listen(8787, "127.0.0.1", () => console.log("api local em http://127.0.0.1:8787"));
