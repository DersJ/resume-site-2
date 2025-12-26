htmx Progressive Enhancement Plan

 Overview

 Refactor Django blog app to use htmx for faster in-app navigation, starting with high-impact
 areas: blog pagination, filtering/sorting, and comments.

 Approach: Progressive enhancement with URL history support, subtle loading indicators, and
 jQuery-to-htmx migration.

 ---
 Phase 1: Setup htmx

 1.1 Add htmx Library

 File: templates/base.html
 - Add htmx CDN script (v1.9.10) before closing </body> tag
 - Position: After Bootstrap JS, before custom scripts

 1.2 Create htmx Styles

 File: static/styles/htmx.scss (new)
 - Loading states (.htmx-request, .htmx-swapping, .htmx-settling)
 - Smooth transitions with opacity changes
 - Loading indicators

 File: static/styles/base.scss
 - Import htmx.scss

 ---
 Phase 2: Blog List Pagination

 2.1 Extract Partial Template

 File: templates/post_list_content.html (new)
 - Extract post loop (lines 52-89) and pagination (lines 91-107) from post_list.html
 - Add htmx attributes to pagination links:
   - hx-get="?page=N"
   - hx-target="#post-list-container"
   - hx-swap="innerHTML"
   - hx-push-url="true" (for URL history)
   - hx-indicator="#loading-indicator"

 2.2 Update Main Template

 File: templates/post_list.html
 - Wrap content in <div id="post-list-container">{% include "post_list_content.html" %}</div>
 - Add loading indicator with Bootstrap spinner

 2.3 Modify View for htmx Detection

 File: blog/views.py - post_list() function (line 160)
 - Check request.headers.get('HX-Request')
 - If htmx: return render(request, "post_list_content.html", context)
 - Otherwise: return full page (graceful degradation)

 ---
 Phase 3: Filtering & Sorting

 3.1 Create htmx-enabled JavaScript

 File: static/js/sortFilterHtmx.js (new)
 - Replace sortFilter.js logic with htmx.ajax() calls
 - Functions: toggleTagHtmx(slug), applySortHtmx(value)
 - Keep URL manipulation helpers (removeFromSearchParams, addToSearchParams)
 - Add htmx:afterSwap event listener to update active filter states

 3.2 Update Template Event Handlers

 File: templates/post_list.html
 - Change tag onclick: toggleTagHtmx(this.dataset.slug)
 - Change sort onchange: applySortHtmx(this.options[this.selectedIndex].value)
 - Replace old sortFilter.js script with sortFilterHtmx.js

 3.3 View Already Supports Query Params

 - No changes needed - existing post_list() handles ?tag= and ?sortBy=

 ---
 Phase 4: Comment Deletion

 4.1 Update Comment Template

 File: templates/comment.html
 - Replace delete button with htmx attributes:
   - hx-delete="/blog/comment/delete/{{ comment.id }}/"
   - hx-target="closest .comment"
   - hx-swap="outerHTML"
   - hx-confirm="Are you sure..."

 4.2 Modify Delete View

 File: blog/views.py - comment_delete() function (line 231)
 - Check request.headers.get('HX-Request')
 - If htmx: return render(request, "comment_deleted.html", context)
 - Otherwise: return HTTP 204 (backward compatibility)

 4.3 Create Deleted Comment Template

 File: templates/comment_deleted.html (new)
 - Show placeholder: "Comment by {user} deleted"
 - Maintains visual feedback

 4.4 Deprecate jQuery Code

 File: static/js/comment.js
 - Comment out or remove deleteComment() function
 - Keep countChars() for character counter

 ---
 Phase 5: Comment Submission

 5.1 Update Comments Template

 File: templates/comments.html
 - Add htmx attributes to form (line 7):
   - hx-post="{{ request.path }}"
   - hx-target="#comments-list"
   - hx-swap="afterbegin" (new comment at top)
   - hx-on::after-request="if(event.detail.successful) this.reset()"
 - Wrap comments loop in <div id="comments-list"> (line 16)

 5.2 Create New Comment Template

 File: templates/comment_new.html (new)
 - Single line: {% include "comment.html" with comment=comment %}

 5.3 Modify Post Detail View

 File: blog/views.py - post_detail() function (line 110)
 - After saving comment, check request.headers.get('HX-Request')
 - If htmx: return render(request, "comment_new.html", {"comment": comment})
 - Otherwise: redirect as usual

 5.4 Update Character Counter

 File: static/js/comment.js
 - Add htmx:afterSwap listener to reset count to 0

 ---
 Phase 6: Loading UX

 6.1 CSS Already Created

 - Done in Phase 1.2 (htmx.scss)

 6.2 Add Scroll Behavior

 File: static/js/sortFilterHtmx.js
 - Add htmx:beforeSwap listener to save scroll position
 - Add htmx:afterSwap listener:
   - Pagination: restore scroll position
   - Filter/sort: smooth scroll to top

 6.3 Error Handling

 File: static/js/sortFilterHtmx.js (or new htmxHelpers.js)
 - Add htmx:responseError listener for server errors
 - Add htmx:sendError listener for network errors
 - Display user-friendly error messages

 ---
 Phase 7: Testing & Cleanup

 7.1 Manual Testing Checklist

 - Pagination works without reload, URL updates
 - Back/forward buttons navigate correctly
 - Tag filtering works, multiple tags selectable
 - Sorting works (newest/oldest/popular)
 - Comment deletion shows confirmation, updates UI
 - Comment submission adds to top, form clears
 - JavaScript disabled: all features work (full reload)
 - Mobile responsive
 - Cross-browser (Chrome, Firefox, Safari)

 7.2 Remove Old JavaScript

 File: static/js/sortFilter.js
 - Delete or archive (replaced by sortFilterHtmx.js)

 7.3 Optional Consolidation

 - Consider merging htmx JavaScript into single htmxHelpers.js
 - Keep code organized and maintainable

 ---
 Critical Files Summary

 New Files (6):

 1. templates/post_list_content.html - Blog list partial
 2. templates/comment_deleted.html - Deleted comment placeholder
 3. templates/comment_new.html - New comment partial
 4. static/styles/htmx.scss - Loading states & transitions
 5. static/js/sortFilterHtmx.js - Filter/sort with htmx
 6. static/js/htmxHelpers.js - (Optional) Error handlers & utilities

 Modified Files (7):

 1. templates/base.html - Add htmx script tag
 2. templates/post_list.html - Use partial, add container & indicator
 3. templates/comment.html - htmx delete button
 4. templates/comments.html - htmx form, wrap comments
 5. blog/views.py - Detect HX-Request, return partials (3 functions)
 6. static/styles/base.scss - Import htmx.scss
 7. static/js/comment.js - Update char counter, deprecate delete

 Deprecated Files (1):

 1. static/js/sortFilter.js - Replaced by sortFilterHtmx.js

 ---
 Success Metrics

 Performance:
 - 60-80% reduction in payload size for pagination/filtering
 - 40-60% faster perceived navigation
 - Smooth transitions with subtle loading indicators

 User Experience:
 - No full page reloads for navigation, filtering, comments
 - URL updates for bookmarking and sharing
 - Browser back/forward buttons work correctly
 - Graceful degradation (works without JavaScript)

 Code Quality:
 - Cleaner separation: htmx handles UI, Django handles data
 - Reduced jQuery dependency
 - Maintainable, progressive enhancement approach

 ---
 Implementation Order

 1. Phase 1 - Setup (quick wins)
 2. Phase 2 - Pagination (highest impact, test htmx workflow)
 3. Phase 3 - Filtering/sorting (builds on Phase 2)
 4. Phase 4 - Comment deletion (migrate from jQuery)
 5. Phase 5 - Comment submission (better UX)
 6. Phase 6 - Polish (loading states, error handling)
 7. Phase 7 - Testing & cleanup

 Each phase is independently testable and can be deployed incrementally.