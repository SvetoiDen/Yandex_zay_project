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

function stringGen(len) {
	var text = "";
	
	var charset = "abcdefghijklmnopqrstuvwxyz0123456789";
	charset = charset.toUpperCase();
	
	for (var i = 0; i < len; i++)
	  text += charset.charAt(Math.floor(Math.random() * charset.length));
	
	return text;
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


async function createFinalPost() {
	let name = document.getElementById('name').value
	let desc = document.getElementById('description').value
	let listContent = document.getElementById('content__structure').children
	let id = stringGen(6)

	if (name == "") {
		alert('Вы не ввели имя поста')
		return
	} else if (desc == "") {
		alert('Вы не ввели описание поста')
		return
	} else if (listContent.length == 0) {
		alert("Вы не добавили контента в посте")
		return
	}

	console.log(listContent);
	const loader = document.getElementById('loader-overlay');
	loader.style.display = "block"
	
	let contentList = [];
	let i = 0;
	for (const textCon of listContent) {
		if (textCon.tagName.toLowerCase() == "textarea") {
			tag = "";
			if (textCon.id == "textPost") {
				tag = "p";
			} else {
				tag = "h2";
			}
			contentList.push(`<${tag}>${textCon.value}</${tag}>`)
		} else {
			const dataImg = await fetch('/data/add_image', {
				method: "POST",
				headers: {'Content-Type': 'application/json'},
				body: JSON.stringify(
					{
						"post_id": id,
						"pos": i,
						"image": textCon.children.item(0).alt
					}
				),
			})
			
			contentList.push(`img_${textCon.children.item(0).getAttribute('type')}`)
			i++;
		}
	}

	let data = {
		"id": id,
		"name": `${name}`,
		"desc": `${desc}`,
		"content": contentList
	}

	tg.sendData(JSON.stringify(data))
	tg.close()
}
tg.expand()