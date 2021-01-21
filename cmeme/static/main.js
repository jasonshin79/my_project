function showMemes(keyword) {
    $.ajax({
        type: "GET",
        url: "/meme",
        data: {"keyword_give": keyword},
        success: function (response) {
            if (response["result"] == "success") {
                $('#cards-box').empty()
                let memes = response['data']
                for (let i = 0; i < memes.length; i++) {
                    let title = memes[i]['title']
                    let url = memes[i]['url']
                    let comment = memes[i]['comment']
                    let like = memes[i]['like']

                    let temp = `<div class="card">
                                    <iframe class="card-img-top" width="360" height="200"
                                            src="${url}" alt="Card image cap">
                                    </iframe>
                                    <div class="card-body">
                                        <a href="${url}" class="card-title">${title}</a>
                                        <p class="card-text">${comment}</p>
                                        <button class="icon" onclick="like('${url}','${i}')"><img id="icon" src="/static/heart.png"/>
                                        <span id="like-${i}">${like}</span></button>
                                        <button class="icon"><img id="icon" src="/static/bubbleComment.png"/>
                                        </button>
                                        <button class="icon"><img id="icon" src="/static/share.png"/>
                                        </button>
                                    </div>
                                </div>`
                    $('#cards-box').append(temp)
                }
            }
        }
    })
}