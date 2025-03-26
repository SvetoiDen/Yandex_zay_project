function openPost() {
	let news = document.getElementById('content_news');
	news.style.display = "none";

	let menu = document.getElementById('menuSite');
	menu.style.display = "none"

	let post = document.getElementById('content_post');
	post.style.display = "block";

	document.getElementById('content__line').style.display = "none"

	window.scrollTo(0,0)
}

function closePost() {
	let news = document.getElementById('content_news');
	news.style.display = "block";

	let menu = document.getElementById('menuSite');
	menu.style.display = "flex"

	document.getElementById('content__line').style.display = "block"

	let post = document.getElementById('content_post');
	post.style.display = "none";
}

const tg = window.Telegram.WebApp;
let nameTg = document.getElementById('nameTg');
let dataTg = document.getElementById('dataTg');
let imgTg = document.getElementById('avatarTg');

tg.ready()
nameTg.innerText = `${tg.initDataUnsafe.user.first_name}`
dataTg.innerText = `@${tg.initDataUnsafe.user.username}`
imgTg.setAttribute('src', `${tg.initDataUnsafe.user.photo_url}`)

function createFinalPost() {
	let name = document.getElementById('name').value
	let desc = document.getElementById('description').value
	let listContent = document.getElementById('content__structure').getElementsByTagName('textarea')
	let contentList = [];
	for (const textAr of listContent) {
		tag = "";
		if (textAr.id == "textPost") {
			tag = "p";
		} else {
			tag = "h2";
		}
		contentList.push(`<${tag}>${textAr.value}</${tag}>`)
	}

	let data = {
		"name": `${name}`,
		"desc": `${desc}`,
		"content": contentList
	}

	tg.sendData(JSON.stringify(data))
	tg.close()
}
tg.expand()