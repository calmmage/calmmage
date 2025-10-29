.PHONY: new-blog
new-blog:
	@read -p "Enter blog title: " title; \
	slug=$$(echo "$$title" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-'); \
	date=$$(date +%Y-%m-%d); \
	filepath="web/app/blog/posts/$$slug.md"; \
	echo "---" > "$$filepath"; \
	echo "title: \"$$title\"" >> "$$filepath"; \
	echo "date: $$date" >> "$$filepath"; \
	echo "tags: []" >> "$$filepath"; \
	echo "published: true" >> "$$filepath"; \
	echo "---" >> "$$filepath"; \
	echo "" >> "$$filepath"; \
	echo "Your content here..." >> "$$filepath"; \
	echo "Created: $$filepath"
