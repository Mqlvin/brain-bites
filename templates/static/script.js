function scrollNext() {
    stopVideos();

    let currentScroll = (document.getElementsByClassName("chapter")[0].style.marginTop);
    if(currentScroll == '') {
        currentScroll = 0;
    } else {
        currentScroll = Math.abs(parseInt(currentScroll));
    }
    currentScroll += 100
    document.getElementsByClassName("chapter")[0].style.marginTop = (parseInt("-" + currentScroll.toString().toString()) + "vh");

    setTimeout(() => {
        let videoContainersId = document.querySelectorAll("div.chapter div div video");

            for(let i = 0; i < videoContainersId.length; i++) {
                if(videoContainersId[i].getBoundingClientRect().top < document.documentElement.clientHeight && videoContainersId[i].getBoundingClientRect().top > 0) {
                    playVideo(videoContainersId[i]);
                    break;
                }
            }
    }, 600);
}

function scrollPrevious() {
    stopVideos();

    let currentScroll = (document.getElementsByClassName("chapter")[0].style.marginTop);
    if(currentScroll == '') {
        currentScroll = 0;
    } else {
        currentScroll = Math.abs(parseInt(currentScroll));
    }
    currentScroll -= 100
    document.getElementsByClassName("chapter")[0].style.marginTop = (parseInt("-" + currentScroll.toString().toString()) + "vh");

    setTimeout(() => {
        let videoContainersId = document.querySelectorAll("div.chapter div div video");

            for(let i = 0; i < videoContainersId.length; i++) {
                if(videoContainersId[i].getBoundingClientRect().top < document.documentElement.clientHeight && videoContainersId[i].getBoundingClientRect().top > 0) {
                    playVideo(videoContainersId[i]);
                    break;
                }
            }
    }, 600);
}

function stopVideos() {
    let videoElements = document.getElementsByTagName("video");
    for(let i = 0; i < videoElements.length; i++) {
        videoElements[i].pause();
        if(videoElements[i].currentTime != 0) {
            setTimeout(() => {
                videoElements[i].currentTime = 0;
            }, 600); // needs to match ms of transition func
        }
    }
}



function playVideo(element) {
    element.play();
}




function toggleHelp() {
    if(document.getElementById("help-box") == undefined) {
        showHelp();
    } else {
        hideHelp();
    }
}


function showHelp() {
}

function hideHelp() {
}
