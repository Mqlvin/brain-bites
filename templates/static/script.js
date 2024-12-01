function scrollNext() {
    hideHelp();
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
    hideHelp();
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




function toggleHelp(idx) {
    if(document.getElementById("help-box") == undefined) {
        showHelp(idx);
    } else {
        hideHelp();
    }
}


function showHelp(idx) {
    let helpBoxElement = document.createElement("div");
    helpBoxElement.id = "help-box";
    helpBoxElement.classList.add("help-box");

    helpBoxElement.innerHTML = htmlHelpElement.replace("{TEXT}", jsonSummary[idx]);
    helpBoxElement.style.opacity = "0";
    helpBoxElement.style.top = (my + 5) + "px";
    helpBoxElement.style.left = (mx + 5) + "px";

    document.body.appendChild(helpBoxElement);

    setTimeout(() => {
        helpBoxElement.style.opacity = "1";
    }, 0);

    
}

function hideHelp() {
    if(document.getElementById("help-box") != undefined) {
        document.getElementById("help-box").style.opacity = "0";
        setTimeout(() => {
            document.getElementById("help-box").remove();
        }, 300);
    }
}


let mx = 0;
let my = 0;

document.addEventListener("mousemove", (e) => {
    mx = e.clientX;
    my = e.clientY;

    if(document.getElementById("help-box") != undefined) {
        let helpBoxElement = document.getElementById("help-box");
        helpBoxElement.style.top = (my + 5) + "px";
        helpBoxElement.style.left = (mx + 5) + "px";
    }
});


let score = 0;
function incrementScore() {
    score++;
    let scoreText = document.getElementById("final-text");
    scoreText.innerHTML = "You scored " + score.toString() + " of 5 on the quiz!<br>Keep going for gold! 🥇";

}
