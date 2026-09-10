with open('index.html', 'r') as f:
    content = f.read()

# Need to also declare trainingUrl
content = content.replace(
    '                    const driveUrl = links.drive;',
    '                    const driveUrl = links.drive;\n                    const trainingUrl = links.training;'
)

injection = """                            ${trainingUrl && html`
                              <a
                                href=${trainingUrl.startsWith('http') ? trainingUrl : `https://${trainingUrl}`}
                                target="_blank"
                                rel="noreferrer"
                                className="inline-flex items-center gap-1 rounded-xl bg-amber-50 border border-amber-200 px-2.5 py-1.5 text-[11px] font-bold text-amber-800 hover:bg-amber-100 transition"
                              >
                                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/><path d="M15 14v-4"/><path d="M12 14v-2"/><path d="M9 14v-3"/></svg>
                                <span>Slide Đào Tạo</span>
                                <${ExternalLink} size=${10} />
                              </a>
                            `}
                            ${driveUrl && html`"""

content = content.replace(
    '                            ${driveUrl && html`',
    injection
)

with open('index.html', 'w') as f:
    f.write(content)
