// ======================================================
// Todo List 페이지 전용 JS
// - 목록 조회
// - 좋아요/북마크/댓글(조회/등록)
// - 페이지네이션
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    const LOGIN_PAGE_URL = "/login/"; // ✅ (유지) 로그인 페이지 URL
    let currentPage = 1;              // ✅ (유지)

    
    if (!window.api) { // ✅ [추가됨] window.api 존재 확인
        console.error("window.api가 없습니다. base.html에서 static/js/api.js가 로드됐는지 확인하세요.");
        alert("설정 오류: api.js가 로드되지 않았습니다.");
        return;
    }

    // ✅ [추가됨] JWT access 토큰이 없으면 바로 로그인 이동(선택 로직)
    // (토큰이 있는데 만료된 경우는 401에서 처리)
    const access = localStorage.getItem("access_token");
    if (!access) {
        console.log("access_token 없음 → 로그인 이동");
        window.location.href = LOGIN_PAGE_URL;
        return;
    }

    // ✅ [추가됨] 401/403 처리 로직을 함수로 분리 (기존 interceptor 대체)
    // ✅ 응답에서 401/403이면 로그인으로 (3단계용: refresh 자동화는 5단계에서)
    function handleAuthError(err) {
        const status = err.response?.status;
        if (status === 401 || status === 403) {
            console.log("인증 실패(401/403) → 토큰 삭제 후 로그인 이동");

            // ✅ [추가됨] 토큰 정리(선택)
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            window.location.href = LOGIN_PAGE_URL;
        }
        return Promise.reject(err);
    }

    /* -------------------------------------------------------
      5) interaction API 엔드포인트 문자열 생성기
      - todoId만 넣으면 URL이 만들어짐
      - 현재는 interaction 앱 APIView 방식 URL을 사용 중
    -------------------------------------------------------- */
    const InteractionAPI = {
        like: (todoId) => `/interaction/like/${todoId}/`,
        bookmark: (todoId) => `/interaction/bookmark/${todoId}/`,
        comment: (todoId) => `/interaction/comment/${todoId}/`,
        commentList: (todoId) => `/interaction/comment/${todoId}/list/`, // (필요 시)
    };



    function loadPage(page) {
        // ✅ [수정됨] 기존: api.get(...) → 세션 기반
        // api.get(`/todo/viewsets/view/?page=${page}`)  // ❌ [삭제됨]

        // ✅ [수정됨] 변경: window.api.get(...) → JWT 토큰 기반
        // ✅ 이제 api.js에서 Authorization: Bearer <access_token> 자동 부착됨
        window.api.get(`/todo/viewsets/view/?page=${page}`)
            .then(res => {
                const data = res.data;

                renderTodos(data.data || data.results || []);
                updatePaginationUI(data);

                currentPage = data.current_page || page;
            })
            .catch(err => {
                // ✅ [수정됨] 기존: console.error("페이지 로드 실패", err) 단순 처리
                // ✅ 변경: 인증 오류면 handleAuthError로 로그인 이동 처리
                handleAuthError(err).catch(() => {}); // ✅ [추가됨] 인증 실패 처리
                console.error("페이지 로드 실패", err.response?.data || err.message); // ✅ [수정됨] 로그 더 자세히
            });
    }

    function renderTodos(todos) {
        const container = document.querySelector(".todocontainer");
        container.innerHTML = "";

        if (!todos || todos.length === 0) {
            container.innerHTML = "<p>등록된 Todo 없음</p>";
            return;
        }

        todos.forEach(todo => {
            const div = document.createElement("div");
            div.className = "todo-item";
            div.dataset.id = todo.id;

            // ✅ 이미지 표시 로직은 그대로 유지
            const imageSrc = todo.image
                ? (todo.image.startsWith("http") ? todo.image : `${location.origin}${todo.image}`)
                : "";

            /* ---------------------------------------------------
              like/bookmark/comment 관련 값 기본값 처리
              - 서버가 null/undefined를 주는 경우 대비
            ---------------------------------------------------- */
            const likeCount = Number(todo.like_count ?? 0);
            const bookmarkCount = Number(todo.bookmark_count ?? 0);
            const commentCount = Number(todo.comment_count ?? 0);

            const isLiked = Boolean(todo.is_liked ?? false);
            const isBookmarked = Boolean(todo.is_bookmarked ?? false);




            div.innerHTML = `
                <p><strong>작성자:</strong> ${todo.username ?? ""}</p>
                <p><strong>제목:</strong> ${todo.name ?? ""}</p>
                <p><strong>설명:</strong> ${todo.description ?? ""}</p>
                <p><strong>완료 여부:</strong> ${(todo.complete ? "완료" : "미완료")}</p>
                <p><strong>exp:</strong> ${todo.exp ?? 0}</p>
                ${imageSrc ? `<img src="${imageSrc}" style="max-width:200px;">` : ""}
                <hr>
        
                <!-- 액션 버튼 영역 -->
                <div class="todo-actions" style="display:flex; gap:10px; align-items:center; margin-top:10px;">
                    <!-- 좋아요 버튼 -->
                    <button class="btn-like" type="button"
                        data-id="${todo.id}"
                        aria-pressed="${isLiked}"
                        style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                        <span class="icon">${isLiked ? "❤️" : "🤍"}</span>
                        <span class="count">${likeCount}</span>
                    </button>

                    <!-- 북마크 버튼 -->
                    <button class="btn-bookmark" type="button"
                        data-id="${todo.id}"
                        aria-pressed="${isBookmarked}"
                        style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                        <span class="icon">${isBookmarked ? "🔖" : "📑"}</span>
                        <span class="count">${bookmarkCount}</span>
                    </button>

                    <!-- 댓글 버튼 -->
                    <button class="btn-comment" type="button"
                        data-id="${todo.id}"
                        style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                        <span class="icon">💬</span>
                        <span class="count">${commentCount}</span>
                    </button>
                </div>

                <!-- 댓글 입력 영역(토글로 보이게 함) -->
                <div class="comment-box" style="display:none; margin-top:10px;">
                    <textarea class="comment-text" rows="3" style="width:100%;"></textarea>
                    <button class="comment-submit" data-id="${todo.id}">등록</button>
                </div>

                <!-- 댓글이 화면에 쌓일 영역 -->
                <div class="comment-list" style="margin-top:8px;"></div>

                <hr>
            `;

            /* ---------------------------------------------------
              카드 클릭 → 상세 페이지 이동
              단, 좋아요/북마크/댓글 영역 클릭은 상세 이동 방지
              (버튼 눌렀는데 detail로 넘어가면 UX가 나쁨)
            ---------------------------------------------------- */






            div.addEventListener("click", (e) => {
                // 버튼/댓글 입력 영역 클릭이면 상세 이동 금지
                if (e.target.closest(".todo-actions") || e.target.closest(".comment-box")) return;

                // 그 외 영역 클릭 시 상세 이동
                window.location.href = `/todo/detail/${todo.id}/`;
            });

            // 컨테이너에 카드 추가
            container.appendChild(div);
            loadComments(todo.id, div);
        });
    }

    async function loadComments(todoId, card) {
        const listEl = card.querySelector(".comment-list");
        if (!listEl) return;
        
        const res = await window.api.get(InteractionAPI.commentList(todoId));
        const comments = res.data || [];

        // 기존 댓글 목록 초기화
        listEl.innerHTML = "";

        // 댓글 배열을 순회하면서 화면에 댓글 생성
        comments.forEach(c => {
            const item = document.createElement("div");
            item.className = "comment-item";
            item.style.padding = "6px 0";

            // 댓글 내용 표시
            // username → 작성자
            // content → 댓글 내용
            item.innerHTML = `<div style="font-size:14px;">
            <strong>${c.username ?? ""}</strong> : ${c.content ?? ""}
            </div>`;

            // 댓글을 댓글 목록 영역에 추가
            listEl.appendChild(item);
        });
    }    

    function updatePaginationUI(data) {
        const current = data.current_page ?? currentPage ?? 1;
        const total =
            data.page_count ??
            (typeof data.count === "number" && data.results
                ? Math.ceil(data.count / data.results.length)
                : "?");

        document.getElementById("pageInfo").innerText = `${current} / ${total}`;

        document.getElementById("prevBtn").disabled = !(data.previous);
        document.getElementById("nextBtn").disabled = !(data.next);
    }

    /* =========================================================
      9) 이벤트 위임 (document 한 곳에서 버튼 클릭 처리)
      - 동적으로 생성된 todo 카드에도 클릭 이벤트가 적용됨
    ========================================================= */
    document.addEventListener("click", async (e) => {

        /* ------------------------
          (1) 좋아요 버튼 처리
        ------------------------- */
        const likeBtn = e.target.closest(".btn-like");
        if (likeBtn) {
            e.stopPropagation(); // 카드 클릭(상세 이동) 막기
            e.preventDefault();

            const todoId = likeBtn.dataset.id;

            try {
                // 서버에 좋아요 토글 요청
                const res = await window.api.post(InteractionAPI.like(todoId));
                const { liked, like_count } = res.data;

                // UI 즉시 반영(아이콘/숫자)
                likeBtn.setAttribute("aria-pressed", String(liked));
                likeBtn.querySelector(".icon").textContent = liked ? "❤️" : "🤍";
                likeBtn.querySelector(".count").textContent = Number(like_count ?? 0);

            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("좋아요 실패:", err.response?.data || err.message);
                alert("좋아요 실패");
            }
            return; // 다른 분기 처리 방지
        }

        /* ------------------------
          (2) 북마크 버튼 처리
        ------------------------- */
        const bookmarkBtn = e.target.closest(".btn-bookmark");
        if (bookmarkBtn) {
            e.stopPropagation();
            e.preventDefault();

            const todoId = bookmarkBtn.dataset.id;

            try {
                const res = await window.api.post(InteractionAPI.bookmark(todoId));
                const { bookmarked, bookmark_count } = res.data;

                // UI 반영
                bookmarkBtn.setAttribute("aria-pressed", String(bookmarked));
                bookmarkBtn.querySelector(".icon").textContent = bookmarked ? "🔖" : "📑";
                bookmarkBtn.querySelector(".count").textContent = Number(bookmark_count ?? 0);

            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("북마크 실패:", err.response?.data || err.message);
                alert("북마크 실패");
            }
            return;
        }

        /* ------------------------
          (3) 댓글 버튼 클릭 → 입력창 토글
        ------------------------- */
        const commentBtn = e.target.closest(".btn-comment");
        if (commentBtn) {
            e.stopPropagation();
            e.preventDefault();

            const card = commentBtn.closest(".todo-item");
            const box = card.querySelector(".comment-box");

            // display 토글
            box.style.display = (box.style.display === "none" || !box.style.display) ? "block" : "none";
            return;
        }

        /* ------------------------
          (4) 댓글 등록 처리
        ------------------------- */
        const submitBtn = e.target.closest(".comment-submit");
        if (submitBtn) {
            e.stopPropagation();
            e.preventDefault();

            const todoId = submitBtn.dataset.id;
            const card = submitBtn.closest(".todo-item");
            const textarea = card.querySelector(".comment-text");
            const content = textarea.value.trim();

            // 빈 댓글 방지
            if (!content) return;

            try {
                // 서버에 댓글 등록 요청
                const res = await window.api.post(InteractionAPI.comment(todoId), { content });
                const saved = res.data; // 서버가 (username, content 등) 응답한다고 가정

                // 1) 화면에 댓글 DOM 추가
                const listEl = card.querySelector(".comment-list");
                const item = document.createElement("div");
                item.className = "comment-item";
                item.style.padding = "6px 0";
                item.innerHTML = `
                    <div style="font-size:14px;">
                        <strong>${saved.username ?? "me"}</strong> : ${saved.content}
                    </div>
                `;
                listEl.prepend(item);

                // 2) 댓글 수 +1 (서버에서 count를 따로 안 주는 경우 대비)
                const countEl = card.querySelector(".btn-comment .count");
                countEl.textContent = Number(countEl.textContent || 0) + 1;

                // 3) 입력창 초기화 + 입력창은 유지(계속 입력하기 편하게)
                textarea.value = "";
                card.querySelector(".comment-box").style.display = "block";

            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("댓글 등록 실패", err.response?.data || err.message);
                alert("댓글 등록 실패");
            }
            return;
        }
    });

    /* =========================================================
      10) 페이지네이션 버튼 이벤트
    ========================================================= */
    document.getElementById("prevBtn").addEventListener("click", () => {
        // 현재 페이지가 2 이상이면 이전 페이지 로드
        if (currentPage > 1) loadPage(currentPage - 1);
    });

    document.getElementById("nextBtn").addEventListener("click", () => {
        // 다음 페이지 로드(서버가 next=false면 버튼이 disabled 됨)
        loadPage(currentPage + 1);
    });

    /* =========================================================
      11) Todo 생성 페이지 이동
    ========================================================= */
    document.getElementById("createBtn").addEventListener("click", () => {
        window.location.href = "/todo/create/";
    });

    /* =========================================================
      12) 최초 1페이지 로드
    ========================================================= */
    loadPage(1);
});