# Todo List for Chat List Implementation

- [ ] Implement chat list caching
- [ ] Save timestamp with cached chat list
- [ ] Add cache validation (older than 1 day check)
- [ ] Add --refresh flag to force reload chat list
- [ ] Implement time-based stats for all chat categories (last 30 days activity)
- [ ] Implement size-based stats
- [ ] Fix JSON serialization for Telethon Dialog objects (current implementation will
  fail)
- [ ] Add cache check in get_chat_list() function (marked as todo in code)
- [x] print stats, don't print the chats