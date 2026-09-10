with open('index.html', 'r') as f:
    content = f.read()

# Add to the parsed project modal
injection = """                              </div>
                              <div className="flex items-center gap-2">
                                <span className="w-24 text-ink/40 flex-shrink-0">Slide Đào tạo:</span>
                                <span className="font-mono text-amber-700 truncate">${parsedResult.project.links.training || 'Không có'}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="w-24 text-ink/40 flex-shrink-0">Drive Tài liệu:</span>"""

content = content.replace(
"""                              </div>
                              <div className="flex items-center gap-2">
                                <span className="w-24 text-ink/40 flex-shrink-0">Drive Tài liệu:</span>""",
injection
)

# Add to the project card (BrokerInventory and ProjectCard components)
# I need to find where "Drive Tài liệu" button is rendered.
