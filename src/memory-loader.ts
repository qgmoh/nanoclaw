/**
 * Memory + STATE loader for NanoClaw agents.
 *
 * Implements the session start protocol from docs/MEMORY_STATE_SYSTEM.md:
 *
 *   1. Inject INDEX.md — agent reads it to decide which 1-2 files to load
 *   2. Inject active STATE if one exists (i != "done") — agent resumes from "i"
 *   3. Agent loads the relevant memory files itself based on INDEX guidance
 *
 * Only INDEX.md + STATE are injected by the host (~20–120 tokens). The agent
 * does the selective loading, keeping per-session overhead at the spec target
 * of ~320–520 tokens rather than always loading everything.
 */
import fs from 'fs';
import path from 'path';

import { resolveGroupFolderPath } from './group-folder.js';
import { logger } from './logger.js';

/**
 * Build a context block containing INDEX.md and any active STATE.
 * Returns an empty string if neither exists.
 */
export function buildMemoryContext(groupFolder: string): string {
  const groupDir = resolveGroupFolderPath(groupFolder);
  const parts: string[] = [];

  // --- INDEX.md (always loaded — ~20 tokens) ---
  const indexPath = path.join(groupDir, 'memory', 'INDEX.md');
  if (fs.existsSync(indexPath)) {
    try {
      const content = fs.readFileSync(indexPath, 'utf-8').trim();
      if (content) {
        parts.push(`### memory/INDEX.md\n${content}`);
      }
    } catch (err) {
      logger.warn({ groupFolder, err }, 'Failed to read memory INDEX.md');
    }
  }

  // --- Active STATE (most recently modified file where i != "done") ---
  const stateDir = path.join(groupDir, 'state');
  if (fs.existsSync(stateDir)) {
    const stateFiles = fs
      .readdirSync(stateDir)
      .filter((f) => f.endsWith('.json'))
      .map((f) => ({
        name: f,
        mtime: fs.statSync(path.join(stateDir, f)).mtimeMs,
      }))
      .sort((a, b) => b.mtime - a.mtime);

    for (const { name } of stateFiles) {
      try {
        const raw = fs.readFileSync(path.join(stateDir, name), 'utf-8');
        const state = JSON.parse(raw);
        if (state.i && !String(state.i).startsWith('done')) {
          parts.push(
            `### Active Task STATE — resume from field "i"\n\`\`\`json\n${JSON.stringify(state, null, 2)}\n\`\`\``,
          );
          logger.info(
            { groupFolder, task: state.t, next: state.i },
            'Active STATE found — injecting into prompt',
          );
          break; // Only the most recent active state
        }
      } catch (err) {
        logger.warn(
          { groupFolder, file: name, err },
          'Failed to read state file',
        );
      }
    }
  }

  if (parts.length === 0) return '';

  return `<context>\n${parts.join('\n\n')}\n</context>\n\n`;
}
