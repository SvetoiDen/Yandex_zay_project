function createText() {
	let textarea = document.createElement('textarea')
	textarea.placeholder = "Текст"
	textarea.cols = 35
	textarea.rows = 3
	textarea.name = 'textPost'
	textarea.id = 'textPost'
	textarea.className = 'textArea Text'
	textarea.style.resize = 'none'
	textarea.required = true
	let contentSctructure = document.getElementById('content__structure')
	contentSctructure.appendChild(textarea)
}

function createH2() {
	let textarea = document.createElement('textarea')
	textarea.cols = 15
	textarea.rows = 3
	textarea.name = 'textH2'
	textarea.id = 'textH2'
	textarea.className = 'textArea H2'
	textarea.placeholder = "Заголовок"
	textarea.style.resize = 'none'
	textarea.required = true
	let contentSctructure = document.getElementById('content__structure')
	contentSctructure.appendChild(textarea)
}

function deleteCreate() {
	let contentCreate = document.getElementById('content__structure').getElementsByTagName('textarea')
	if (contentCreate.length > 0) {
		contentCreate.item(contentCreate.length - 1).remove()
		let contentSctructure = document.getElementById('content__structure')
	}
}