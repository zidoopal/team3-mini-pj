const signupBtn = document.querySelector("#signup-button");
const emailValidationBtn = document.querySelector("#email-validation-button");
const authBtn = document.querySelector(".verification_button");

// 페이지 시작 시
$(() =>{
    setTimeout(() => {
        $('#signup-email').fadeIn()    
    }, 50);
    setTimeout(() => {
        $('#signup-password').fadeIn()
    }, 100);
    setTimeout(() => {
        $('#signup-confirmPassword').fadeIn()
    }, 150)
    setTimeout(() => {
        $('#signup-nickname').fadeIn()
    }, 200)
    setTimeout(() => {
        $('.hidden').fadeIn()
        $('.right__footer').css({"display": "flex","justify-content":"end"})
    }, 250)
    
    
    
    
    
    
})

const signup = () => {
    const email = $("#email").val();
    const password = $("#password").val();
    const confirmPassword = $("#confirmPassword").val();
    const nickname = $("#nickname").val();

    let formData = new FormData();
    formData.append("email_give", email);
    formData.append("password_give", password);
    formData.append("confirmPassword_give", confirmPassword);
    formData.append("nickname_give", nickname);


    fetch('/signup', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        let error_html = ``
        // 이메일 입력 여부 검증
        if (data['msg'] == '이메일을 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }
        // 이메일 유효성 검증
        else if (data['msg'] == '유효하지 않은 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }
        // 이메일 중복 검증
        else if (data['msg'] == '이미 등록된 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }
        // 비밀번호 입력 검증
        else if (data['msg'] == '비밀번호를 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-password').append(error_html)
            $('#signup-password').children('#password').addClass('input_validation_error')
            $('#signup-password').children('#password').val('')
        }
        // 비밀번호 길이 검증
        else if (data['msg'] == '비밀번호는 5자리 이상 20자리 이하로 해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-password').append(error_html)
            $('#signup-password').children('#password').addClass('input_validation_error')
        }
        // 비밀번호 일치 여부 검증
        else if (data['msg'] == '비밀번호가 일치하지 않습니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-confirmPassword').append(error_html)
            $('#signup-confirmPassword').children('#confirmPassword').addClass('input_validation_error')
        }
        else if (data['msg'] == '닉네임을 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }
        // 닉네임 길이 검증
        else if (data['msg'] == '닉네임은 20자리 이하로 해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }
        // 닉네임 중복 검증
        else if (data['msg'] == '이미 등록된 닉네임 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }
        else if(data['msg'] == '이메일 인증이 필요합니다!'){
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }

        else if (data['msg'] == '회원가입이 완료되었습니다!') {
            alert('회원가입이 완료되었습니다. 로그인 해 주세요!')
            window.location.href = "/login"
        }



    });
}

const emailValidation = () => {
    const email = $("#email").val();
    let formData = new FormData();
    formData.append("email_give", email);

    fetch('/signup/email-verification', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        $(".verification_input").val('')
        let error_html = ``
        // 이메일 입력 여부 검증
        if (data['msg'] == '이메일을 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }
        // 이메일 유효성 검증
        else if (data['msg'] == '유효하지 않은 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        }
        // 이메일 중복 검증
        else if (data['msg'] == '이미 등록된 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email .email_input').addClass('input_validation_error')
        } else if (data['msg'] == '이메일 검증 완료.') {
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')

            $('#email').prop('disabled', true)
            $('#email-validation-button').prop('disabled', true)
            $('.verification_container').fadeIn();
            
            // 이메일 전송
            fetch('/signup/send-email', { method: "POST", body: formData })
        }
    })
}

const emailAuth = () =>{
    const email = $('#email').val();
    const accessCode = $('.verification_input').val();
    let formData = new FormData()
    formData.append('email_give',email);
    formData.append('accessCode_give',accessCode);

    fetch('/signup/verify-auth-code', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        let error_html = ``
        if(data['msg'] == '이메일 인증 성공'){
            let comp_html = `<div class="comp_msg">인증 완료</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')

            $('.verification_container').append(comp_html)
            $('.verification_button').prop('disabled', true)
            $('.verification_input').prop('disabled', true)

        } else if(data['msg'] == '인증번호가 일치하지 않습니다.'){
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('.verification_container').append(error_html)
            $('.verification_input').addClass('input_validation_error')
        } else if(data['msg'] == '인증번호가 만료되었습니다.'){
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('.verification_container').append(error_html)
            $('.verification_input').addClass('input_validation_error')

            $('#email-validation-button').prop('disabled', false)
        }
    })
}

signupBtn.addEventListener("click", signup);
emailValidationBtn.addEventListener("click", emailValidation);
authBtn.addEventListener("click", emailAuth)