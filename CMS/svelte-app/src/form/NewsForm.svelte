<script>
    import {writable} from "svelte/store";
    import 'tw-elements'

    export let newsData;
    export let formNet;

    formNet.news = newsData



    function swapUp(i) {
        if (i !== 0) {
            const tmp = newsData[i - 1]
            newsData[i - 1] = newsData[i]
            newsData[i] = tmp
        }
    }

    function swapDown(i) {
        if (i !== newsData.length - 1) {
            const tmp = newsData[i + 1]
            newsData[i + 1] = newsData[i]
            newsData[i] = tmp
        }
    }

    const newsFormValues = writable({
        title: "",
        content: "",
        href: "",
        position: newsData.length + 1
    })

    function newsFormSubmit() {
        const obj = {
            title: $newsFormValues.title,
            content: $newsFormValues.content,
            href: $newsFormValues.href
        }
        let position = $newsFormValues.position

        if (formStatus !== -1)
            del(formStatus)

        newsData.splice(position - 1, 0, obj)
        newsData = newsData

        console.log(newsData, newsData.length + 1)
        $newsFormValues.title = ""
        $newsFormValues.content = ""
        $newsFormValues.href = ""
        $newsFormValues.position = newsData.length + 1
    }

    let formStatus = -1 //-1: adding new news; <=0 : editing selected index

    function edit(i) {
        const obj = newsData[i]
        formStatus = i
        $newsFormValues.title = obj.title
        $newsFormValues.content = obj.content
        $newsFormValues.href = obj.href
        $newsFormValues.position = i + 1
    }

    function del() {
        newsData.splice(formStatus, 1)
        newsData = newsData
        cancel()
    }

    function cancel() {
        $newsFormValues.title = ""
        $newsFormValues.content = ""
        $newsFormValues.href = ""
        $newsFormValues.position = newsData.length + 1
        formStatus = -1
    }
</script>

<div class="border border-gray-300 m-10 px-10 pb-10">
    <h1 class = "p-5">News Form</h1>
    <div class = "flex flex-row">
    <form on:submit|preventDefault={()=>newsFormSubmit()} class="w-1/3  border border-gray-300">
        <h3 class="m-4">
            {#if formStatus === -1}
                Adding new element:
            {:else}
                Editing element (title:{newsData[formStatus].title}, href: {newsData[formStatus].href}):
            {/if}
        </h3>
        <div class="m-4"><label for="titleInput">title<input id="titleInput" type="text"
                                                             bind:value={$newsFormValues.title}
                                                             class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/></label>
        </div>
        <div class="m-4"><label for="contentInput">content<textarea id="contentInput" type="text"
                                                                    bind:value={$newsFormValues.content}
                                                                    class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"></textarea>
        </label></div>
        <div class="m-4"><label for="hrefInput">href<input id="hrefInput" type="text" bind:value={$newsFormValues.href}
                                                           class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/>
        </label></div>
        <div class="m-4"><label for="positionInput">position<input id="positionInput" type="number" min="1"
                                                                   max={formStatus===-1?newsData.length+1:newsData.length}
                                                                   bind:value={$newsFormValues.position}
                                                                   class=" form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/>
        </label></div>


        <div class="flex flex-row">

            <button type="submit"
                    class="m-4 px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out">
                Submit
            </button>

            {#if formStatus !== -1}
                <button on:click={del} type="button"
                        class="inline-block px-6 py-2 border-2 border-red-600 text-red-600 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out">
                    Delete
                </button>
                <button on:click={cancel} type="button"
                        class="inline-block px-6 py-2 border-2 border-yellow-500 text-yellow-500 font-medium text-xs leading-tight uppercase rounded hover:bg-black hover:bg-opacity-5 focus:outline-none focus:ring-0 transition duration-150 ease-in-out">
                    Cancel
                </button>
            {/if}
        </div>

    </form>

    <table class="ml-4 content-list w-2/3">
        <tr>
            <th class="border border-slate-300">title</th>
            <th class="border border-slate-300">content</th>
            <th class="border border-slate-300">href</th>
            <th class="border border-slate-300">edit</th>
        </tr>
        {#each newsData as content, i}
            <tr>
                <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">{content.title}</td>
                <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4">{content.content}</td>
                <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">{content.href}</td>
                <td class="border border-slate-300 text-sm text-gray-900 font-light px-3 py-1 whitespace-nowrap">
                    <div class="flex flex-row justify-around">
                        <button on:click={()=>edit(i)} class="edit px-4 uppercase">edit</button>
                        <div class="flex flex-col">
                        </div>
                    </div>
                </td>
            </tr>
        {/each}
    </table>
    </div></div>

<style>
    .edit:hover,
    .arrow:hover svg {
        color: #00e9ff;
    }

    .content-list tr:nth-child(2) .arrow:first-child svg {
        opacity: 0.3;
    }

    .content-list tr:last-child .arrow:last-child svg {
        opacity: 0.3;
    }

    .content-list tr:nth-child(2) .arrow:first-child:hover svg {
        opacity: 0.3;
        color: black;
    }

    .content-list tr:last-child .arrow:last-child:hover svg {
        opacity: 0.3;
        color: black;
    }
</style>