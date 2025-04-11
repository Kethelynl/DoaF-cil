document.addEventListener("DOMContentLoaded", function(){
    const element = document.querySelectorAll(".reveal");
    const element2 = document.querySelectorAll(".reveal-sub");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if(entry.isIntersecting){
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.2}
    );

    element.forEach((element) => observer.observe(element));
    element2.forEach((element2) => observer.observe(element2));
});