<script>
    import {writable} from "svelte/store";
    import 'tw-elements'

    export let headerData;
    export let formNet;

    formNet.header = headerData

    let links = headerData.menu.links
    formNet.header.menu.links = links


    function swapUp(i) {
        if (i !== 0) {
            const tmp = links[i - 1]
            links[i - 1] = links[i]
            links[i] = tmp
        }
    }

    function swapDown(i) {
        if (i !== links.length - 1) {
            const tmp = links[i + 1]
            links[i + 1] = links[i]
            links[i] = tmp
        }
    }

    const newsFormValues = writable({
        text: "",
        href: "",
        position: links.length + 1,
        dropDown: false
    })

    function newsFormSubmit() {
        const obj = {
            text: $newsFormValues.text,
            href: $newsFormValues.href,
            dropDown: $newsFormValues.dropDown
        }
        let position = $newsFormValues.position

        if (formStatus !== -1)
            del(formStatus)

        links.splice(position - 1, 0, obj)
        links = links

        console.log(links, links.length + 1)
        $newsFormValues.text = ""
        $newsFormValues.href = ""
        $newsFormValues.dropDown = false
        $newsFormValues.position = links.length + 1
    }

    let formStatus = -1 //-1: adding new news; <=0 : editing selected index

    function edit(i) {
        const obj = links[i]
        formStatus = i
        $newsFormValues.text = obj.text
        $newsFormValues.href = obj.href
        $newsFormValues.dropDown = obj.dropDown ? true : false
        $newsFormValues.position = i + 1
    }

    function del() {
        links.splice(formStatus, 1)
        links = links
        cancel()
    }

    function cancel() {
        $newsFormValues.text = ""
        $newsFormValues.href = ""
        $newsFormValues.dropDown = false
        $newsFormValues.position = links.length + 1
        formStatus = -1
    }
</script>
<div class="border border-gray-300 m-10 px-10 pb-10">
    <h1 class="p-5">Header Form</h1>
    <div class="flex flex-row">
        <form on:submit|preventDefault={()=>newsFormSubmit()} class="w-1/3  border border-gray-300">
            <h3 class="m-4">
                {#if formStatus === -1}
                    Adding new element:
                {:else}
                    Editing element (text:{links[formStatus].text}, href: {links[formStatus].href}):
                {/if}
            </h3>
            <div class="m-4"><label for="textInput">text<input id="textInput" type="text"
                                                               bind:value={$newsFormValues.text}
                                                               class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/></label>
            </div>
            <div class="m-4"><label for="hrefInput">href<input id="hrefInput" type="text"
                                                               bind:value={$newsFormValues.href}
                                                               class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/>
            </label></div>
            <div class="m-4"><label for="positionInput">position<input id="positionInput" type="number" min="1"
                                                                       max={formStatus===-1?links.length+1:links.length}
                                                                       bind:value={$newsFormValues.position}
                                                                       class=" form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"/>
            </label></div>
            <div class="m-4">
                <input class="form-check-input appearance-none h-4 w-4 border border-gray-300 rounded-sm bg-white checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200 mt-1 align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer"
                       type="checkbox" id="flexCheckDefault" bind:value={$newsFormValues.dropDown}>
                <label class="form-check-label inline-block text-gray-800" for="flexCheckDefault">
                    Drop-Down
                </label>
            </div>


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
                <th class="border border-slate-300">text</th>
                <th class="border border-slate-300">href</th>
                <th class="border border-slate-300">dropDown</th>
                <th class="border border-slate-300">edit</th>
            </tr>
            {#each links as content, i}
                <tr>
                    <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">{content.text}</td>
                    <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">{content.href}</td>
                    <td class="border border-slate-300 text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">{content.dropDown?true:false}</td>
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
    </div>
</div>

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