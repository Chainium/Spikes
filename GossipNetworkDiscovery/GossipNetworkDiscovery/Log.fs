﻿namespace Chainium.Network.Gossip

open System 

module Log = 

    let private log logType o =
        sprintf "[%s] %s | %s" (DateTimeOffset.Now.ToString("yyyy-MM-dd HH:mm:ss.fff zzz")) logType (o.ToString())    
    
    let info o = log "INFO" o |> printfn "%s"
    let warning o = log "WARNING" o |> printfn "%s"
    let error o = log "ERROR" o |> eprintfn "%s"

    let infof format = Printf.ksprintf info format
    let warningf format = Printf.ksprintf warning format
    let errorf format = Printf.ksprintf error format
