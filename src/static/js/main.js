function unsecuredCopyToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
    } catch (err) {
        console.error('Unable to copy to clipboard', err);
    }
    document.body.removeChild(textArea);
}

document.addEventListener('DOMContentLoaded', () => {
    const btnCopyList = document.querySelectorAll('.link-copy');
    const loadingWrapper = document.getElementById('loadingWrapper');
    const resultWrapper = document.getElementById('resultWrapper');

    btnCopyList.forEach((elem) => {

        const tooltip = new bootstrap.Tooltip(elem, {'trigger': 'manual', 'html': true, 'customClass': 'custom-tooltip', 'title': '<div><i class="bi bi-check-lg"></i> <span>Co!py</span></div>'});

        elem.addEventListener('click', () => {
            copyTargetId = elem.getAttribute('copy-target');
            copyTarget = document.getElementById(copyTargetId);

            if (location.protocol === 'http:') {
                unsecuredCopyToClipboard(copyTarget.innerText);
                tooltip.show();
                setTimeout(() => {
                    tooltip.hide();
                }, 2000);
            } else {
                window.navigator.clipboard.writeText(copyTarget.innerText)
                    .then(() => {
                        tooltip.show();
                        setTimeout(() => {
                            tooltip.hide()
                        }, 2000);
                    })
                    .catch(err => console.error('Failed to copy: ', err));
            }
        });
    });

    const url = "/api/v1/server-ip";
    fetch(url)
    .then((response) => response.json())
    .then((resp) => {
        if (resp.result === 'success') {
            const resultIpv4 = document.getElementById('resultIpv4');
            const ipv4 = resp.data.ipv4;

            resultIpv4.innerText = ipv4 ? ipv4 : "Query failed";

            if ('ipv6' in resp.data) {
                const resultIpv6 = document.getElementById('resultIpv6');
                const ipv6 = resp.data.ipv6;

                resultIpv6.innerText = ipv6 ? ipv6 : "Query failed";
            }
        } else {
            throw new Error("API returned failure status");
        }

        loadingWrapper.classList.add('is-none');
        resultWrapper.classList.remove('is-none');
    })
    .catch((error) => {
        console.log(error)
        loadingWrapper.innerHTML = `<h5 class="text-center mt-2">Failed.</h5><br>Error message:<br>${error}`;
    });
})