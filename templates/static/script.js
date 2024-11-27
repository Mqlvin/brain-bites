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

    let chapterIndex = parseInt(currentScroll / 100);
    try {
        if(document.getElementsByClassName("scrollable-content")[0].children[chapterIndex].children[0].children[0].children[0].tagName == "VIDEO") {
            console.log("playing video")
            playVideo(chapterIndex);
        }
    } catch {} // doesn't matter not a video anyway
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

    let chapterIndex = parseInt(currentScroll / 100);
    try {
        if(document.getElementsByClassName("scrollable-content")[0].children[chapterIndex].children[0].children[0].children[0].tagName == "VIDEO") {
            console.log("playing video")
            playVideo(chapterIndex);
        }
    } catch {} // not video anyway
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



function playVideo(chapterIndex) {
    console.log("video-" + (chapterIndex - 1));
    let newVideo = document.getElementById("video-" + (chapterIndex - 1));
    newVideo.play();
}
