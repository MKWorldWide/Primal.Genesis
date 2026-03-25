/**
 * @description Custom hook for automated changelog and memory updates
 * @changelog [v1.0.0] Initial implementation of self-upgrade hook
 * @prime-directive Provides automated documentation updates and changelog management
 * @lessons-learned Automated documentation requires careful versioning and atomic updates
 * @usage import { useSelfUpgrade } from '../hooks/useSelfUpgrade';
 * @dependencies React, fs-extra, path
 * @performance Updates are batched and performed asynchronously
 * @security No sensitive data is exposed in changelog or memory updates
 * @accessibility Updates are logged with clear timestamps and version information
 * @example
 * ```tsx
 * const { updateChangelog, updateMemories } = useSelfUpgrade();
 * 
 * // Update changelog
 * await updateChangelog({
 *   version: '1.0.0',
 *   changes: ['Added new feature', 'Fixed bug']
 * });
 * 
 * // Update memories
 * await updateMemories({
 *   type: 'feature',
 *   description: 'Implemented new feature'
 * });
 * ```
 */

import { useCallback } from 'react';
import fs from 'fs-extra';
import path from 'path';

interface ChangelogEntry {
  version: string;
  changes: string[];
  timestamp?: string;
}

interface MemoryEntry {
  type: 'feature' | 'bug' | 'improvement';
  description: string;
  timestamp?: string;
}

export const useSelfUpgrade = () => {
  const updateChangelog = useCallback(async (entry: ChangelogEntry) => {
    try {
      const changelogPath = path.join(process.cwd(), 'CHANGELOG.md');
      const timestamp = entry.timestamp || new Date().toISOString();
      
      const changelogEntry = `
## [${entry.version}] - ${timestamp}
${entry.changes.map(change => `- ${change}`).join('\n')}
`;
      
      await fs.appendFile(changelogPath, changelogEntry);
      console.log(`[Self-Upgrade] Changelog updated for version ${entry.version}`);
    } catch (error) {
      console.error('[Self-Upgrade] Failed to update changelog:', error);
    }
  }, []);

  const updateMemories = useCallback(async (entry: MemoryEntry) => {
    try {
      const memoriesPath = path.join(process.cwd(), '.cursor', 'memories.md');
      const timestamp = entry.timestamp || new Date().toISOString();
      
      const memoryEntry = `
[${timestamp}] ${entry.type.toUpperCase()}: ${entry.description}
`;
      
      await fs.appendFile(memoriesPath, memoryEntry);
      console.log(`[Self-Upgrade] Memories updated for ${entry.type}`);
    } catch (error) {
      console.error('[Self-Upgrade] Failed to update memories:', error);
    }
  }, []);

  const updateLessonsLearned = useCallback(async (entry: MemoryEntry) => {
    try {
      const lessonsPath = path.join(process.cwd(), '.cursor', 'lessons-learned.md');
      const timestamp = entry.timestamp || new Date().toISOString();
      
      const lessonEntry = `
[${timestamp}] ${entry.type.toUpperCase()}: ${entry.description}
`;
      
      await fs.appendFile(lessonsPath, lessonEntry);
      console.log(`[Self-Upgrade] Lessons learned updated for ${entry.type}`);
    } catch (error) {
      console.error('[Self-Upgrade] Failed to update lessons learned:', error);
    }
  }, []);

  return {
    updateChangelog,
    updateMemories,
    updateLessonsLearned
  };
}; 