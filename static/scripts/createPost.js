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

function createImg() {
	let divContent = document.getElementsByClassName('input-file-label')
	if (!(divContent.length < 1)) {
		alert("Нельзя добавить еще картинку, т.к вы не приняли предыдущую")
		return
	}

	let divImg = document.createElement('div')
	divImg.className = "input-file"
	divImg.id = "input-file"

	let labelImg = document.createElement('label')
	labelImg.className = "input-file-label"
	labelImg.id = "input-file-label"
	labelImg.textContent = "Выберите фотографию"

	let areaimg = document.createElement('input')
	areaimg.required = true
	areaimg.type = "file"
	areaimg.name = "fileImg"
	areaimg.id = "fileImg"
	areaimg.accept = "image/*"
	areaimg.onchange = function(event) {
		const file = event.target.files[0];
		if (file) {
		  const reader = new FileReader();
		  reader.onload = function(e) {
			const preview = document.createElement('img');
			preview.src = e.target.result;
			preview.style.display = 'block';
			preview.id = "preview"
			preview.style.maxWidth = "300px"
			preview.style.marginTop = "15px"
			preview.alt = e.target.result.replace("data:"+ file.type +";base64,", '')
			preview.setAttribute('type', file.type)
	
			let divImg = document.getElementsByClassName('input-file')
			let labelImg = document.getElementById('input-file-label')
			divImg.item(divImg.length - 1).appendChild(preview)
			labelImg.remove()
		  };
		  reader.readAsDataURL(file);
		}
	}
	
	labelImg.appendChild(areaimg);
	divImg.appendChild(labelImg)

	let contentSctructure = document.getElementById('content__structure')
	contentSctructure.appendChild(divImg)
}

function deleteCreate() {
	let content = document.getElementById('content__structure').children
	if (content.length > 0) {
		content.item(content.length - 1).remove()
	}
}
