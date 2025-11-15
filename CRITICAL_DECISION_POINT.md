# CRITICAL FIX REQUIRED

**Commander - The GUI file has structural JavaScript errors that require complete reconstruction.**

**Current Errors:**
1. `let recognition` declared twice
2. Functions defined but not in global scope  
3. Event listeners failing
4. Multiple undefined function errors

**File Size:** 1951 lines
**Complexity:** Too high for incremental fixes

**RECOMMENDATION:**

Deploy clean working version from templates:
- Use last working commit
- OR build from minimal template
- Add MCP panel feature to clean base

**Actions Taken:**
- ✅ Backup created: `index.html.broken_backup`
- ✅ Duplicate `recognition` variable removed
- ⏳ Need complete file reconstruction

**Next Steps:**
1. Confirm approach: restore or rebuild?
2. Deploy MCP panel to working base
3. Test all functions systematically

**Alternative:**
Create separate MCP_PANEL.html for testing, then merge

**Awaiting Commander decision on approach.**
