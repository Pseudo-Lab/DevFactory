// Mobile Menu Toggle
const menuToggle = document.getElementById('menu-toggle');
const closeBtn = document.getElementById('close-menu');
const menuOverlay = document.getElementById('mobile-menu-overlay');
const mobileLinks = document.querySelectorAll('.mobile-nav-link');

function openMenu() {
    menuOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scroll
}

function closeMenu() {
    menuOverlay.classList.remove('active');
    document.body.style.overflow = ''; // Restore scroll
}

if (menuToggle) menuToggle.addEventListener('click', openMenu);
if (closeBtn) closeBtn.addEventListener('click', closeMenu);

mobileLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
});

// Member Data & Core Functions
const teamMembers = [
    {
        name: "김수현",
        enName: "KIM SOOHYUN",
        role: "BUILDER",
        position: "TPM / INFRA",
        status: "Active",
        contribution: "Builder",
        gen: "10th, 11th",
        desc: "가짜연구소의 개발 문화를 설계하고 운영합니다. DevFactory의 빌더로서 클라우드 인프라와 프로젝트 관리를 총괄합니다.",
        image: "/members/soohyun.png",
        github: "https://github.com/soohyunme",
        linkedin: "https://www.linkedin.com/in/soohyun-dev"
    },
    {
        name: "김예신",
        enName: "KIM YESIN",
        role: "BUILDER",
        position: "Backend Developer",
        status: "Active",
        contribution: "Builder",
        gen: "10th, 11th",
        desc: "백엔드 개발을 담당하며 견고한 시스템 아키텍처를 설계합니다. 10기와 11기 빌더로서 활동하고 있습니다.",
        image: "/members/yesin.jpg",
        github: "https://github.com/yesinkim",
        linkedin: "https://www.linkedin.com/in/bailando/"
    },
    {
        name: "김승규",
        enName: "KIM SEUNGKYU",
        role: "BUILDER",
        position: "Frontend Developer",
        status: "Active",
        contribution: "Builder",
        gen: "10th, 11th",
        desc: "사용자 중심의 프론트엔드 환경을 구축합니다. DevFactory의 다양한 웹 서비스를 매력적으로 시각화합니다.",
        image: "/members/seungkyu.jpg",
        github: "https://github.com/ed-kyu",
        linkedin: "https://www.linkedin.com/in/seungkyu-kim-9088a21b1/"
    },
    {
        name: "황윤희",
        enName: "HWANG YUNHEE",
        role: "BUILDER",
        position: "Product Owner",
        status: "Active",
        contribution: "Builder",
        gen: "11th",
        desc: "프로덕트의 방향성을 제시하고 기획을 담당합니다. 11기 빌더로서 DevFactory의 성장을 이끕니다.",
        image: "https://github.com/yunhee1.png",
        github: "https://github.com/yunhee1",
        linkedin: "https://www.linkedin.com/in/uni-po/"
    },
    {
        name: "최유진",
        enName: "CHOI YUJIN",
        role: "RUNNER",
        position: "Product Owner",
        status: "Active",
        contribution: "Runner",
        gen: "11th",
        desc: "11기 러너로서 프로덕트 오너 역할을 수행하며 새로운 아이디어를 구체화합니다.",
        image: "/members/yujin.jpg",
        github: "https://github.com/yujin37",
        linkedin: "https://www.linkedin.com/in/yujin37/"
    },
    {
        name: "석종일",
        enName: "SEOK JONGIL",
        role: "RUNNER",
        position: "Frontend Developer",
        status: "Active",
        contribution: "Runner",
        gen: "11th",
        desc: "웹 기술에 열정을 가진 11기 러너입니다. 프론트엔드 개발자로서 프로젝트에 기여하고 있습니다.",
        image: "https://github.com/daclouds.png",
        github: "https://github.com/daclouds",
        linkedin: "https://www.linkedin.com/in/daclouds/"
    },
    {
        name: "정현준",
        enName: "JUNG HYUNJUN",
        role: "RUNNER",
        position: "Backend Developer",
        status: "Active",
        contribution: "Runner",
        gen: "11th",
        desc: "서버 사이드 로직과 데이터베이스를 다루는 11기 러너입니다. 안정적인 서비스 제공에 힘씁니다.",
        image: "https://github.com/hu6r1s.png",
        github: "https://github.com/hu6r1s",
        linkedin: "https://www.linkedin.com/in/hu6r1s/"
    },
    {
        name: "한나연",
        enName: "HAN NAYEON",
        role: "RUNNER",
        position: "Backend Developer",
        status: "Active",
        contribution: "Runner",
        gen: "11th",
        desc: "11기 러너로서 백엔드 개발에 참여하고 있습니다. 효율적인 코드와 협업을 중요하게 생각합니다.",
        image: "https://github.com/HanNayeoniee.png",
        github: "https://github.com/HanNayeoniee",
        linkedin: "https://www.linkedin.com/in/nayeon-han/"
    },
];

let currentIndex = 0;

function updateDisplay(index) {
    const member = teamMembers[index];

    // Select elements
    const visual = document.getElementById('member-visual');
    const name = document.getElementById('member-name');
    const bgName = document.getElementById('member-bg-name');
    const role = document.getElementById('role-tag');
    const desc = document.getElementById('member-desc');
    const pos = document.getElementById('stat-position');
    const contr = document.getElementById('stat-contribution');
    const gen = document.getElementById('stat-gen');
    const socialContainer = document.getElementById('member-social');

    // Add animation classes
    const panel = document.getElementById('info-panel');
    const visualContainer = visual.parentElement;

    panel.classList.remove('fade-in');
    visualContainer.classList.remove('fade-in');
    if (bgName) bgName.classList.remove('fade-in');

    // Trigger reflow to restart animation
    void panel.offsetWidth;
    void visualContainer.offsetWidth;
    if (bgName) void bgName.offsetWidth;

    // Update content
    visual.src = member.image;
    name.textContent = member.name;
    if (bgName) bgName.textContent = member.enName;
    role.textContent = member.role;

    // Add runner class for styling (Builder keeps default cyan)
    role.className = 'role-tag';
    if (member.role === 'RUNNER') {
        role.classList.add('runner');
    }

    desc.textContent = member.desc;
    pos.textContent = member.position;
    contr.textContent = member.contribution;
    gen.textContent = member.gen;

    // Update social links (restore bar buttons)
    socialContainer.innerHTML = '';
    if (member.github) {
        const githubLink = document.createElement('a');
        githubLink.href = member.github;
        githubLink.target = '_blank';
        githubLink.className = 'social-btn';
        githubLink.title = 'GitHub Profile';
        githubLink.innerHTML = `
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.042-1.416-4.042-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span>GitHub</span>
        `;
        socialContainer.appendChild(githubLink);
    }
    if (member.linkedin) {
        const linkedinLink = document.createElement('a');
        linkedinLink.href = member.linkedin;
        linkedinLink.target = '_blank';
        linkedinLink.className = 'social-btn';
        linkedinLink.title = 'LinkedIn Profile';
        linkedinLink.innerHTML = `
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            <span>LinkedIn</span>
        `;
        socialContainer.appendChild(linkedinLink);
    }

    panel.classList.add('fade-in');
    visualContainer.classList.add('fade-in');
    if (bgName) bgName.classList.add('fade-in');

    // Highlight thumbnail
    document.querySelectorAll('.thumb-btn').forEach((btn, i) => {
        if (i === index) btn.classList.add('active');
        else btn.classList.remove('active');
    });
}

function initThumbnails() {
    const container = document.getElementById('thumb-grid');
    teamMembers.forEach((member, index) => {
        const btn = document.createElement('button');
        btn.className = 'thumb-btn';
        if (index === 0) btn.classList.add('active');

        const img = document.createElement('img');
        img.src = member.image;
        img.alt = member.name;

        btn.appendChild(img);
        btn.addEventListener('click', () => {
            if (currentIndex === index) return;
            currentIndex = index;
            updateDisplay(index);
        });

        container.appendChild(btn);
    });
}

function updateTime() {
    const timeEl = document.getElementById('system-time');
    if (timeEl) {
        const now = new Date();
        timeEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }
}

function nextMember() {
    currentIndex = (currentIndex + 1) % teamMembers.length;
    updateDisplay(currentIndex);
}

function prevMember() {
    currentIndex = (currentIndex - 1 + teamMembers.length) % teamMembers.length;
    updateDisplay(currentIndex);
}

// Initialize
initThumbnails();
updateDisplay(0);
setInterval(updateTime, 1000);
updateTime();

// Section Reveal Animation (Intersection Observer)
const sections = document.querySelectorAll('.full-section');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.15 });

sections.forEach(section => revealObserver.observe(section));

// Visitor Tracking
async function logVisit() {
    try {
        await fetch('/api/stats/visit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: window.location.pathname + window.location.hash,
                userAgent: navigator.userAgent
            })
        });
    } catch (err) {
        console.warn('Visitor tracking failed (server probably not running yet)');
    }
}

logVisit();

// Prev/Next Navigation
document.getElementById('prev-member').addEventListener('click', prevMember);
document.getElementById('next-member').addEventListener('click', nextMember);

// Cross-Platform Swipe Navigation (Touch & Mouse)
let startX = 0;
let isDragging = false;

const teamSect = document.getElementById('team');

// Touch Events
teamSect.addEventListener('touchstart', e => {
    startX = e.changedTouches[0].screenX;
}, { passive: true });

teamSect.addEventListener('touchend', e => {
    const endX = e.changedTouches[0].screenX;
    handleSwipe(startX, endX);
}, { passive: true });

// Mouse Events for PC
teamSect.addEventListener('mousedown', e => {
    startX = e.screenX;
    isDragging = true;
});

teamSect.addEventListener('mouseup', e => {
    if (!isDragging) return;
    const endX = e.screenX;
    handleSwipe(startX, endX);
    isDragging = false;
});

teamSect.addEventListener('mouseleave', () => {
    isDragging = false;
});

function handleSwipe(sX, eX) {
    const swipeThreshold = 50;
    if (eX < sX - swipeThreshold) {
        animateArrowFeedback('next-member');
        nextMember(); // Swipe Left -> Next
    } else if (eX > sX + swipeThreshold) {
        animateArrowFeedback('prev-member');
        prevMember(); // Swipe Right -> Prev
    }
}

function animateArrowFeedback(buttonId) {
    const btn = document.getElementById(buttonId);
    if (btn) {
        btn.classList.add('active');
        setTimeout(() => btn.classList.remove('active'), 200);
    }
}

// Global Keyboard Navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        prevMember();
    } else if (e.key === 'ArrowRight') {
        nextMember();
    }
});
