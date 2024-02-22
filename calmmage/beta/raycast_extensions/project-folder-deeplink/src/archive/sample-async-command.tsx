// // import { Detail } from "@raycast/api";
// // import { getClipboardPath } from './common';
// // async function copyClipboardValue() {
// //     const content = await getClipboardPath();
// //     return <Detail markdown={content} />;
// // }

// // export default {
// //     name: 'sample-async-command',
// //     description: 'Copy Clipboard Value',
// //     // Make the command async
// //     async run() {
// //       // Call your async function here
// //       return await copyClipboardValue();
// //     },
// //   };

// import { Detail, ActionPanel, CopyToClipboardAction } from "@raycast/api";
// import { getClipboardPath } from './common';

// class ClipboardDetail extends React.Component {
//   state = {
//     content: ''
//   }

//   async componentDidMount() {
//     const content = await getClipboardPath();
//     this.setState({ content });
//   }

//   render() {
//     return <Detail markdown={this.state.content} />;
//   }
// }

// export default {
//   name: 'sample-async-command',
//   description: 'Copy Clipboard Value',
//   // Use ClipboardDetail as the render function
//   render: ClipboardDetail,
//   actions: [
//     new ActionPanel([
//       new CopyToClipboardAction({
//         title: "Copy Clipboard Value",
//         content: this.state.content,
//       }),
//     ]),
//   ];
// };