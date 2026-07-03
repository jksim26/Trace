CREATE TABLE IF NOT EXISTS decisions (
    id             TEXT PRIMARY KEY,
    statement      TEXT NOT NULL,
    discipline     TEXT,
    riba_stage     INTEGER,
    author         TEXT,                 -- JSON array of strings
    rationale      TEXT,
    assumptions    TEXT,                 -- JSON array of strings
    brief_ref      TEXT,
    importance     INTEGER,
    valid_from     TEXT,                 -- when true in the world
    valid_to       TEXT,                 -- NULL = currently valid
    recorded_at    TEXT,                 -- when the system learned it
    superseded_at  TEXT,
    superseded_by  TEXT REFERENCES decisions(id),
    status         TEXT NOT NULL DEFAULT 'valid'
                       CHECK (status IN ('valid','superseded','proposed')),
    source_episode TEXT
);

-- Tamper-evident audit chain: every write (add / supersede / verdict) appends
-- an event whose hash covers the previous event's hash — so any later edit to
-- the log breaks the chain and is detectable by verify_audit_chain().
CREATE TABLE IF NOT EXISTS audit_log (
    seq       INTEGER PRIMARY KEY AUTOINCREMENT,
    event     TEXT NOT NULL CHECK (event IN ('add','supersede','verdict')),
    ref       TEXT,                 -- decision id the event concerns
    payload   TEXT NOT NULL,        -- canonical JSON of what was written
    at        TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    hash      TEXT NOT NULL
);

-- The decision court's record: every verdict is persisted, so the "defensible
-- record" the court produces actually exists on the trail (never deleted).
CREATE TABLE IF NOT EXISTS court_records (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id      TEXT REFERENCES decisions(id),
    breaks_id        TEXT REFERENCES decisions(id),
    verdict          TEXT NOT NULL CHECK (verdict IN ('REJECT','ALLOW')),
    citation         TEXT,
    for_argument     TEXT,
    against_argument TEXT,
    rationale        TEXT,
    created_at       TEXT NOT NULL
);
